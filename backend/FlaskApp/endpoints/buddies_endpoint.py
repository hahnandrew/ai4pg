import time
from configs import CONFIGS
import requests;
from flask import Blueprint,request
from urllib.parse import urlparse
from managers.firebase_manager.check_for_authentication import check_for_authentication

from utils.my_util import APIMsgFormat
from handlers  import buddies_handler

buddies_endpoint =Blueprint("buddies", __name__, url_prefix="/buddies")



@buddies_endpoint.route('/list',methods=['POST'])
def buddies_endpoint_list_buddies():
  data = request.json.get('data',{})
  page_data = buddies_handler.list_buddies(data)
  res = APIMsgFormat(data=page_data,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200
