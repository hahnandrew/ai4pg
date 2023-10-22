import gzip
import json
import os
import random

import requests
from utils.api_exceptions import APIServerError
from utils.env_vars import ENV_VARS
from utils.singleton_exception import SingletonException
from utils.local_deps import  local_deps
local_deps()

class RestDBIOEmailManager():
  init= False
  server_key = ""
  dev_emails = [
    {
      'email':'dev@windmillcode.com'
    }
  ]
  prod_emails = [
    {
      'email':'enrique.r.felix@windmillcode.com'
    }
  ]
  join_waitlist_email_template =""

  def __init__(self,server_key):
    if(self.init):
      raise SingletonException
    else:
      self.init = True
      self.server_key = server_key
      self._init_email_templates()

  def _init_email_templates(self):
    return
    join_waitlist_email_template_path = os.path.join("my_resources/email_templates/join_waitlist.html")
    with open(
      join_waitlist_email_template_path,encoding="utf-8"
    ) as f:
      self.join_waitlist_email_template = f.read()

  def send_email(self,content,sendername="MICHAEL EMMA Community",subject="DEV Subject",to_emails=None):
    headers = {
      "Content-Type": "application/json",
      "x-apikey":self.server_key,
      "Cache-Control": "no-cache"
    }
    default_to_emails = to_emails if to_emails != None else [item['email'] for item in self.dev_emails]
    if(os.getenv("FLASK_BACKEND_ENV") != "DEV"):
      default_to_emails = to_emails if to_emails != None else [item['email'] for item in self.prod_emails]

    req_body={
      "to":default_to_emails,
      "subject":subject,
      "html": content,
      "company": "MICHAEL EMMA",
      "sendername": sendername
    }
    resp =requests.post(
      "https://sessionbyme-dda6.restdb.io/mail",
      data=json.dumps(req_body),
      headers=headers
    )
    if(resp.status_code not in [200,201]):
      raise APIServerError("An error occured while trying to send email")








