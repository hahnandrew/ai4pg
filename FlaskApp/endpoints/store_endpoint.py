import time
from configs import CONFIGS
import requests;
import math
from flask import Blueprint,request
import json
from urllib.parse import urlparse
from managers.firebase_manager.check_for_authentication import check_for_authentication
from utils.api_exceptions import APIServerError
from utils.my_flask_cache import clear_cache_on_request_body_change, my_cache
from utils.my_util import APIMsgFormat
from utils.env_vars import flask_backend_env
from handlers  import store_handler

store_endpoint =Blueprint("store", __name__, url_prefix="/store")


@clear_cache_on_request_body_change(timeout=30000 if flask_backend_env == "DEV" else 3000)
@store_endpoint.route('/products/list',methods=['POST'])
def store_products_list():
  page_data = request.json.get("data")
  page_object = store_handler.list_products(page_data)
  res = APIMsgFormat(data=page_object)
  return res.return_flask_response(),200

@clear_cache_on_request_body_change(timeout=30000 if flask_backend_env == "DEV" else 3000)
@store_endpoint.route('/categories/list',methods=['POST'])
def store_categories_list():
  page_data = request.json.get("data")
  page_object = store_handler.list_categories(page_data)
  res = APIMsgFormat(data=page_object)
  return res.return_flask_response(),200


@store_endpoint.route('/products/purchase',methods=['POST'])
@check_for_authentication(optional=True)
def store_purchase_products(firebase_uid=None,square_uid=None):
  req_body = request.json.get("data")
  payment_link = store_handler.purchase_products(req_body,square_uid)
  res = APIMsgFormat(data=payment_link)
  return res.return_flask_response(),200

@store_endpoint.route('/lto_expirations/update',methods=['POST'])
def store_endpoint_update_lto_expirations():
  data = request.json.get('data',{})


  res = APIMsgFormat(msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200


@store_endpoint.route('/lto_expirations/list',methods=['GET'])
def store_endpoint_list_lto_expirations():
  result_set = store_handler.list_lto_expirations()

  res = APIMsgFormat(data=result_set,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200



