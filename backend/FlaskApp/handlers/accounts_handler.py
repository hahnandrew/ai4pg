

import time
from configs import CONFIGS
from enum import Enum
from utils.api_exceptions import APIAuthorizationError, APIServerError
from utils.iterable_utils import list_get
from utils.print_if_dev import print_if_dev

class AccountsEndpointUsersListTypeEnum(Enum):
    CREATEACCTIFNOTEXISTS = 0


def create_accounts(data,firebase_uid):
  if firebase_uid != data["id"]:
    res = APIAuthorizationError(data["id"])
    return res.return_flask_response()
  try:
    CONFIGS.firebase_manager.set_env_for_user(data["id"])
    sqaure_customer =CONFIGS.square_manager.create_customer(data["id"],data["email"])
  except BaseException as e:

    return APIServerError("An error occured while creating the account {}".format(e)).return_flask_response()
  # data = {
  #   "sqaure_customer_id":sqaure_customer["customer"]["id"]
  # }
  return sqaure_customer["customer"]


def list_accounts(page_dict,firebase_uid):
    api_reference_id =CONFIGS.square_manager.create_reference_id(firebase_uid)

    reference_id =list_get(
      list(filter(lambda x:x["key"] == "reference_id" and x["value"] == api_reference_id,  page_dict["filter"])),
      0
    ).get("value",None)
    if reference_id != api_reference_id:
      # client had the access token but the wrong refernce_id
      res = APIAuthorizationError()
      return res.return_flask_response()

    page_data= None
    while not page_data:
      try:
        page_data = CONFIGS.square_manager.get_customer(page_dict)
      except BaseException as e:
        time.sleep(5)
    if page_dict.get("type",None) == AccountsEndpointUsersListTypeEnum.CREATEACCTIFNOTEXISTS.value:
      if len(page_data.data) == 0:

        page_data.data.append(create_accounts({
          "id":firebase_uid,
          "email":page_dict["email"]
          },firebase_uid))
        page_data.calculate_current_state()

    return page_data
