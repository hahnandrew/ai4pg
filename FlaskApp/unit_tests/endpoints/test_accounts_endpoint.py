

from configs import CONFIGS
from unit_tests.conftest import TestUtils, fake_check_for_authentication



def test_accounts_endpoint_create_accounts(client,monkeypatch):

  monkeypatch.setattr("handlers.accounts_handler.create_accounts",TestUtils.generic_fake)
  response = client.post('/accounts/users/create',json= {
    "data":{}
  })

  assert response.status_code == 200
  assert CONFIGS.endpointMsgCodes["success"]  == response.json['code']
  assert TestUtils.generic_fake_result  == response.json['data']



def test_accounts_endpoint_list_accounts(client,monkeypatch):

  monkeypatch.setattr("handlers.accounts_handler.list_accounts",TestUtils.generic_fake)
  response = client.post('/accounts/users/list',json= {
    "data":{}
  })

  assert response.status_code == 200
  assert CONFIGS.endpointMsgCodes["success"]  == response.json['code']
  assert TestUtils.generic_fake_result  == response.json['data']

