import json
import time
from configs import CONFIGS
from enum import Enum
from firebase_admin.auth import ExportedUserRecord
from utils.api_exceptions import APIAuthorizationError, APIServerError
from utils.iterable_utils import list_get
from utils.wml_libs.pagination import WMLAPIPaginationResponseModel
from utils.env_vars import flask_backend_env

def list_buddies(page_dict):

    page_data = WMLAPIPaginationResponseModel()
    firebase_users = CONFIGS.firebase_manager.list_users(filter_uids=False)
    square_users = []
    if flask_backend_env in ["PROD","PREVIEW"]:
      square_users = CONFIGS.square_manager.list_customers()

    result_set = []
    for user in firebase_users:
      result_set.append({
        "firebase":{
          "id":user.uid,
          "display_name":user.display_name,
          "avatar_url":user.photo_url
        }
      })

    for index0,user in enumerate(square_users):
      user["reference_id"]
      result_set_item = next((x for x in result_set if CONFIGS.square_manager.create_reference_id(
        x.get("firebase").get("id")
        ) ==user["reference_id"]  ), None)
      sqaure_obj= {
          "id":user["id"],
        }
      if result_set_item is not None:
        result_set_item["square"] = sqaure_obj
      else:
        result_set.append({
          "square":sqaure_obj
        })


    page_obj = WMLAPIPaginationResponseModel()
    page_obj.calc_section_based_on_page_details(
      data=result_set,
      page_num=page_dict["page_num"],
      page_size=page_dict["page_size"]
    )
    

    return page_obj
