from configs import CONFIGS
from utils.print_if_dev import print_if_dev

def test_healthcheck(client):
  response = client.get('/healthz/')
  assert "A-OK"  == response.json['msg']
  assert CONFIGS.endpointMsgCodes["success"]  == response.json['code']


def test_mytest_healthcheck(client):
  response = client.get('/healthz/test')
  assert response.request.url  == response.json['msg']
  assert CONFIGS.endpointMsgCodes["success"]  == response.json['code']

