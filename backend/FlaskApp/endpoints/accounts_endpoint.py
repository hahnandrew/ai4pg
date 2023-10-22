import time
from configs import CONFIGS
import requests;
from flask import Blueprint,request
from urllib.parse import urlparse
from managers.firebase_manager.check_for_authentication import check_for_authentication

from utils.my_util import APIMsgFormat
from handlers  import accounts_handler

accounts_endpoint =Blueprint("accounts", __name__, url_prefix="/accounts")

@accounts_endpoint.route('/users/create',methods=['POST'])
@check_for_authentication(square_id_required=False)
def accounts_endpoint_create_accounts(firebase_uid):
  data = request.json.get('data',{})
  resp_data =accounts_handler.create_accounts(data,firebase_uid)
  res = APIMsgFormat(data=resp_data,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200


@accounts_endpoint.route('/users/list',methods=['POST'])
@check_for_authentication(square_id_required=False)
def accounts_endpoint_list_accounts(firebase_uid):
  data = request.json.get('data',{})
  page_data = accounts_handler.list_accounts(data,firebase_uid)
  res = APIMsgFormat(data=page_data,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200
