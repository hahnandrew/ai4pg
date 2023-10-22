import time
from configs import CONFIGS
import requests;
from flask import Blueprint,request
from urllib.parse import urlparse

from utils.my_util import APIMsgFormat
from handlers  import validate_handler

validate_endpoint =Blueprint("validate", __name__, url_prefix="/validate")




@validate_endpoint.route('/eligible',methods=['POST'])
def validate_post_endpoint():
  data = request.json.get('data',{})
  new_data = validate_handler.post_endpoint(data)
  res = APIMsgFormat(data=data, msg=request.url,code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200

@validate_endpoint.route('/',methods=[''])
def validate_endpoint_receive_doc():
  data = request.json.get('data',{})


  res = APIMsgFormat(msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200
