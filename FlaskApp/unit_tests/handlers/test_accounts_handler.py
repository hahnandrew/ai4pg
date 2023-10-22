


# create_accounts
from handlers.accounts_handler import AccountsEndpointUsersListTypeEnum, create_accounts, list_accounts
from unit_tests.conftest import TestUtils
from flask.json import jsonify
from utils.api_exceptions import APIAuthorizationError, APIServerError
from utils.wml_libs.pagination import WMLAPIPaginationRequestModel, WMLAPIPaginationResponseModel
import handlers

class FakeAPIAuthorizationError(APIAuthorizationError):
  def __init__(self,data="Authorization Error"):
    self.data = data
  def return_flask_response(self):
    return {
      "data":self.data,
      "code":self.code
    }

class FakeAPIServerError(APIServerError):
  def __init__(self,data):
    self.data = data
  def return_flask_response(self):
    return {
      "data":self.data,
      "code":self.code
    }

class FakeCONFIGSFirebaseManager():
  def set_env_for_user(self,*args):
    None

class FakeCONFIGSSquareManager():
  def create_customer(self,*args):
    return {
      "customer":"customer"
    }
  def create_reference_id(*args):
    return "create_reference_id"

  def get_customer(*args):
    return WMLAPIPaginationResponseModel()

class FakeCONFIGS():
  firebase_manager = FakeCONFIGSFirebaseManager()
  square_manager = FakeCONFIGSSquareManager()

def set_mocks(monkeypatch):
    monkeypatch.setattr(
    "handlers.accounts_handler.APIAuthorizationError",
    FakeAPIAuthorizationError
  )
    monkeypatch.setattr(
    "handlers.accounts_handler.APIServerError",
    FakeAPIServerError
  )
    monkeypatch.setattr(
    "handlers.accounts_handler.CONFIGS",
    FakeCONFIGS
  )

def test_create_accounts_0(monkeypatch,mocker):
  # firebase_uid != data["id"]:
  # arrange
  set_mocks(monkeypatch)

  firebase_uid = 2
  data = {
    "id":1
  }

  # act
  result =create_accounts(data,firebase_uid)

  # assert
  assert result["data"] == 1
  assert result["code"] == 403



def test_create_accounts_1(monkeypatch,mocker):
  # firebase_uid != data["id"]:
  # arrange


  set_mocks(monkeypatch)
  set_env_for_user_mock = mocker.patch("handlers.accounts_handler.CONFIGS.firebase_manager.set_env_for_user")
  create_customer_mock = mocker.patch("handlers.accounts_handler.CONFIGS.square_manager.create_customer")

  firebase_uid = 2
  data = {
    "id":firebase_uid,
    "email":"firebase_email"
  }

  # act
  result =create_accounts(data,firebase_uid)

  # assert
  assert set_env_for_user_mock.call_count == 1
  assert create_customer_mock.call_count == 1
  # assert result.json == FakeCONFIGSSquareManager().create_customer()

def test_create_accounts_2(monkeypatch,mocker):
  # firebase_uid != data["id"] &&  except BaseException as e is thrown:
  # arrange


  set_mocks(monkeypatch)
  set_env_for_user_mock = mocker.patch("handlers.accounts_handler.CONFIGS.firebase_manager.set_env_for_user")
  create_customer_mock = mocker.patch("handlers.accounts_handler.CONFIGS.square_manager.create_customer")

  firebase_uid = 2
  data = {
    "id":firebase_uid,
  }

  # act
  result =create_accounts(data,firebase_uid)

  # assert
  assert set_env_for_user_mock.call_count == 1
  assert result["code"] == 500



def test_list_accounts_0(monkeypatch,mocker):
  # reference_id != api_reference_id:
  # arrange


  set_mocks(monkeypatch)
  set_env_for_user_mock = mocker.patch("handlers.accounts_handler.CONFIGS.firebase_manager.set_env_for_user")
  create_customer_mock = mocker.patch("handlers.accounts_handler.CONFIGS.square_manager.create_customer")
  create_reference_id_mock = mocker.patch("handlers.accounts_handler.CONFIGS.square_manager.create_reference_id")

  page_dict = WMLAPIPaginationRequestModel(
    filter=[
      {"key":"reference_id","value":"value"}
    ]
  ).to_json()
  firebase_uid = "firebase_uid"

  # act
  result =list_accounts(page_dict,firebase_uid)


  # assert
  assert create_reference_id_mock.call_count == 1
  assert result["code"] == 403



def test_list_accounts_1(monkeypatch,mocker):
  # reference_id == api_reference_id:
  # arrange


  set_mocks(monkeypatch)
  set_env_for_user_mock = mocker.spy(handlers.accounts_handler.CONFIGS.firebase_manager,"set_env_for_user")
  create_customer_mock = mocker.spy(handlers.accounts_handler.CONFIGS.square_manager,"create_customer")
  create_reference_id_mock = mocker.spy(handlers.accounts_handler.CONFIGS.square_manager,"create_reference_id")

  page_dict = WMLAPIPaginationRequestModel(
    filter=[
      {"key":"reference_id","value":FakeCONFIGSSquareManager().create_reference_id()}
    ]
  ).to_json()
  firebase_uid = "firebase_uid"

  # act
  result =list_accounts(page_dict,firebase_uid)


  # assert
  assert create_reference_id_mock.call_count == 1
  assert isinstance(result,WMLAPIPaginationResponseModel)



def test_list_accounts_1(monkeypatch,mocker):
  # reference_id == api_reference_id && page_dict.get("type",None) == AccountsEndpointUsersListTypeEnum.CREATEACCTIFNOTEXISTS.value:
  # arrange


  set_mocks(monkeypatch)
  set_env_for_user_mock = mocker.spy(handlers.accounts_handler.CONFIGS.firebase_manager,"set_env_for_user")
  create_customer_mock = mocker.spy(handlers.accounts_handler.CONFIGS.square_manager,"create_customer")
  create_reference_id_mock = mocker.spy(handlers.accounts_handler.CONFIGS.square_manager,"create_reference_id")
  create_accounts_spy = mocker.spy(handlers.accounts_handler,"create_accounts")

  page_dict = WMLAPIPaginationRequestModel(
    filter=[
      {"key":"reference_id","value":FakeCONFIGSSquareManager().create_reference_id()}
    ]
  ).to_json()
  page_dict["type"] = AccountsEndpointUsersListTypeEnum.CREATEACCTIFNOTEXISTS.value
  page_dict["email"] = "email.com"
  firebase_uid = "firebase_uid"

  # act
  result =list_accounts(page_dict,firebase_uid)


  # assert
  assert create_accounts_spy.call_count == 1
  assert create_reference_id_mock.call_count == 1
  assert isinstance(result,WMLAPIPaginationResponseModel)
  assert len(result.data) == 1




[]
