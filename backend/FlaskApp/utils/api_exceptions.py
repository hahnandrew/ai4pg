from abc import ABC

from utils.local_deps import local_deps
local_deps()
from flask.json import jsonify


class APIError(Exception):
    description = "An error occured"
    """All custom API Exceptions"""
    def __init__(self, desc=None):
      self.description = desc if desc else self.description

    def return_flask_response(self):
      resp_dict = self.__dict__
      resp = jsonify(resp_dict)


      return resp,self.code


class APIAuthenticationError(APIError):
  code = 401
  description = "Authentication Error"

class APIAuthorizationError(APIError):
  code = 403
  description = "Authorization Error"
class APIServerError(APIError):
  code = 500
  description = "The server is having an issue processing the request please contact developer support"

class APIClientError(APIError):
  code = 404
  description = "bad input from the client please have the client review the request for any incorrect params, and/or request body properties and try again"

