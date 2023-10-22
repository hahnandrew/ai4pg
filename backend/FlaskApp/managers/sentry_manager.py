import json
import os
import random
from utils.env_vars import ENV_VARS
from utils.singleton_exception import SingletonException
from utils.local_deps import  local_deps
local_deps()
import sentry_sdk

class SentryManager():
  init= False
  def __init__(self):
    if(self.init):
      raise SingletonException
    else:
      self.init = True


  def init_sentry(self):
    if ENV_VARS.get("FLASK_BACKEND_ENV") == "DEV":
      return
    sentry_sdk.init(
      dsn="https://6cbf3bf3ac3c4659906e0b7036023ac5@o4505122556215296.ingest.sentry.io/4505490809225216",
      environment="Flask_{}".format(ENV_VARS.get("FLASK_BACKEND_ENV")),
      traces_sample_rate=1.0,
    )




