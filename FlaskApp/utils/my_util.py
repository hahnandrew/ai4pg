import secrets
import string
import os
from time import sleep
from urllib.parse import parse_qs, urlencode, urlparse
from configs import CONFIGS
from flask.helpers import make_response
from utils.local_deps import  local_deps
local_deps()
from sqlalchemy import create_engine
import requests
from flask.json import jsonify
import json

from werkzeug.http import parse_cookie
import sendgrid

class APIMsgFormat():
  def __init__ (self,data=None,code=CONFIGS.endpointMsgCodes["success"],access_token=None,msg="OK"):
    if data:
      self.data = data
      if hasattr(self.data,'to_json'):
        self.data = self.data.to_json()
    self.access_token = access_token
    self.msg = msg
    self.code = code

  data ={
    "please ":"provide data in the data property"
  }
  access_token =None
  msg = "OK"
  code = ""

  def return_flask_response(self):
    resp_dict = self.__dict__
    try:
      if resp_dict.get("access_token") == None:
        del resp_dict["access_token"]
    except BaseException as e:
      pass
    resp = make_response(jsonify(resp_dict))

    return resp





def generate_random_string(len =7):
    return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(len))

def turn_query_params_to_object(url):
    parsed_url = urlparse(url)
    return {
        x:y[0] for x,y in parse_qs(parsed_url.query).items()
    }

def turn_cookie_to_object(cookie_list,cookie_name):
    cookie = next(
        (cookie for cookie in cookie_list if cookie_name in cookie),
        None
    )
    return parse_cookie(cookie) if cookie is not None else cookie



def pull_unique_items_from_list(target_list):
  return [x for i, x in enumerate(target_list) if x not in target_list[:i]]

def generate_twillio_sendgrid_email_req_body(from_email,to_emails=[],personalizations_subject="Sample Subject",email_template="Sample Email"):
  return {
    "personalizations":[{
      "to":[{"email":email} for email in to_emails],
      "subject":personalizations_subject
    }],
    "from":{"email":from_email},
    "content":[
      {
        "type": "text/html",
        "value": email_template
      }
    ]
  }



