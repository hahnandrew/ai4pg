import time
from configs import CONFIGS
import requests;
from flask import Blueprint,request
from urllib.parse import urlparse

from utils.my_util import APIMsgFormat
from handlers  import validate_handler

validate_endpoint =Blueprint("validate", __name__, url_prefix="/validate")






@validate_endpoint.route('/receive_rap_sheet',methods=['POST'])
def validate_endpoint_receive_doc():


  data = validate_handler.receive_doc(request.data)
  res = APIMsgFormat(data=data,msg="A-OK",code=CONFIGS.endpointMsgCodes["success"])
  return res.return_flask_response(),200
