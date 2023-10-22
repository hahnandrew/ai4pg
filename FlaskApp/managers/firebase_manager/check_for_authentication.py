from functools import wraps
from configs import CONFIGS
from firebase_admin import auth
from utils.api_exceptions import APIAuthenticationError, APIServerError
from flask import request, jsonify


def check_for_authentication(optional=False,square_id_required=True):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

      access_token = request.json.get("data").get("access_token",None)
      if access_token:
          try:
            decoded_token = auth.verify_id_token(access_token)
            if square_id_required == True:
              square_customer = CONFIGS.square_manager.get_customer_via_firebase_id(decoded_token['uid'])
              if  square_customer.get("id",None) == None:
                return APIServerError("Firebase user does not have a corresponding square customer account").return_flask_response()
              return func(decoded_token["uid"],square_customer["id"], *args, **kwargs)
            else:
              return func(decoded_token["uid"], *args, **kwargs)
          except auth.InvalidIdTokenError:
            return APIAuthenticationError("Invalid ID token.").return_flask_response()
      else:
        if optional == True:
          return func( *args, **kwargs)
        return APIAuthenticationError("Missing ID token.").return_flask_response()
    return wrapper
  return decorator
