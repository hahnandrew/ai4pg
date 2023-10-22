import os
from db.postgres_manager import PostgresManager

from managers.firebase_manager.firebase_manager import FirebaseManager
from managers.openai_manager import OpenAIManager
from managers.restdbio_manager.restdbio_email_manager import RestDBIOEmailManager
from managers.sentry_manager import SentryManager
from managers.square_manager import SquareManager
from managers.watchdog_manager import WatchdogManager
from utils.env_vars import ENV_VARS
from utils.local_deps import  local_deps
from utils.run_cron_tasks import CronTasksRunner
local_deps()

class DevConfigs:

  endpointMsgCodes = {
    'success':'OK',
    'error':'ERROR',
  }

  app ={}
  postgres_manager= None
  # openai_manager = OpenAIManager(ENV_VARS.get("OPENAI_API_KEY_0"))
  # sentry_manager = SentryManager()
  # restdbio_email_manager = RestDBIOEmailManager(ENV_VARS.get("RESTDBIO_SERVER_API_KEY_0"))

  # cron_task_runner =  CronTasksRunner()
  # firebase_manager = FirebaseManager(ENV_VARS)

  def _create_app_info_obj(self,backend_port=5025):

    return {
      'access_control_allow_origin':['https://example.com:4222'],
      'server_name':'example.com:{}'.format(backend_port),
      'domain_name':'https://example.com:{}'.format(backend_port),
      'flask_env':'development',
      'frontend_angular_app_url':'https://example.com:4222',
      'frontend_angular_app_domain':'example.com',
      'backend_port':backend_port
    }

  def __init__(self):
    self.app =self._create_app_info_obj()
    # self.postgres_manager = PostgresManager(ENV_VARS.get("SQLALCHEMY_POSTGRESSQL_0_CONN_STRING"),self)
    # self.square_manager = SquareManager(
    #   ENV_VARS.get("SQUARE_ACCESS_TOKEN_0"),
    #   ENV_VARS.get("SQUARE_LOCATION_NAME_0"),
    #   self
    # )



class TestConfigs(DevConfigs):
  None

class PreviewConfigs(DevConfigs):

  def __init__(self) -> None:
    super().__init__()
    self.app['flask_env'] = 'production'
    self.app['access_control_allow_origin'] = ["https://ui.preview.tooboards.com"]
    self.app.pop('server_name')
    self.app.pop('domain_name')
    self.app['frontend_angular_app_url'] = "https://ui.preview.tooboards.com"
    self.app['frontend_angular_app_domain'] = "ui.preview.tooboards.com"

class ProdConfigs(DevConfigs):

  def __init__(self) -> None:
    super().__init__()
    self.app['flask_env'] = 'production'
    self.app['access_control_allow_origin'] = ["https://tooboards.com","https://www.tooboards.com"]
    self.app.pop('server_name')
    self.app.pop('domain_name')
    self.app['frontend_angular_app_url'] = "https://www.tooboards.com"
    self.app['frontend_angular_app_domain'] = "www.tooboards.com"



CONFIGS:DevConfigs= {
  'PROD':lambda x:ProdConfigs(),
  'PREVIEW':lambda x:PreviewConfigs(),
  'DEV':lambda x:DevConfigs(),
  'TEST':lambda x:TestConfigs(),
}[ENV_VARS.get("FLASK_BACKEND_ENV")](None)











