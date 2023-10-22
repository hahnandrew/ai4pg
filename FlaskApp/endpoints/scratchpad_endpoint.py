import time
from configs import CONFIGS
import requests;
import math
from flask import Blueprint,request
import json
from urllib.parse import urlparse
from managers.firebase_manager.check_for_authentication import check_for_authentication

from utils.my_util import APIMsgFormat
from utils.print_if_dev import print_if_dev
from utils.specific.hash_string import hash_string

from handlers  import accounts_handler,scratchpad_handler
from utils.wml_libs.pagination import WMLAPIPaginationRequestModel

scratchpad_endpoint =Blueprint("scratchpad", __name__, url_prefix="/scratchpad")

@scratchpad_endpoint.route('/users/create',methods=['POST'])
@check_for_authentication(square_id_required=False)
def accounts_endpoint_create_accounts(firebase_uid):
  data = request.json.get('data',{})
  resp_data =accounts_handler.create_accounts(data,firebase_uid)

  res = APIMsgFormat(data=resp_data,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200


@scratchpad_endpoint.route('/admin/users/clear',methods=['DELETE'])
def scratchpad_endpoint_delete_all_users():
  data = request.json.get('data',{})
  scratchpad_handler.delete_all_users(data)
  res = APIMsgFormat(msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200




