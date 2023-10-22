import asyncio
import os
import sys
import traceback

from configs import CONFIGS,ENV_VARS


from utils.my_util import APIMsgFormat
from utils.api_exceptions import APIError
from utils.local_deps import  local_deps
from utils.print_if_dev import print_if_dev
from utils.my_flask_cache import my_cache
local_deps()
from flask.helpers import make_response
from flask.json import jsonify
from flask import Flask, request, redirect
import sqlalchemy
from flask_caching import Cache

# dev additions
from endpoints.healthcheck_endpoint import healthcheck_endpoint

from endpoints.scratchpad_endpoint import scratchpad_endpoint
from endpoints.store_endpoint import store_endpoint
from endpoints.accounts_endpoint import accounts_endpoint
from endpoints.buddies_endpoint import buddies_endpoint

app = Flask(__name__)
app.config.update(
    FLASK_ENV = CONFIGS.app['flask_env'],
    SECRET_KEY=os.environ.get("FLASK_SOCKET_IO_SECRET_KEY"),
    DEBUG = False,
)
if ENV_VARS.get("FLASK_BACKEND_ENV") == "DEV":
  app.config.update(
    DEBUG = True
  )
my_cache.init_app(app)

app.register_blueprint(healthcheck_endpoint)
app.register_blueprint(store_endpoint)
app.register_blueprint(accounts_endpoint)
app.register_blueprint(buddies_endpoint)

if ENV_VARS.get("FLASK_BACKEND_ENV") == "DEV":
  app.register_blueprint(scratchpad_endpoint)

@app.before_request
def upgrade_to_https():
  if not request.is_secure and ENV_VARS.get("FLASK_BACKEND_ENV") == "DEV" :
    if request.method != 'OPTIONS' or 'Access-Control-Request-Method' not in request.headers:
      url = request.url.replace('http://', 'https://', 1)
      code = 301
      return redirect(url, code=code)


@app.after_request
def after_request(response):
  origin =  request.headers.get('Origin',"")

  if origin in CONFIGS.app['access_control_allow_origin'] or CONFIGS.app['access_control_allow_origin'][0] == '*':
    response.headers.add('Access-Control-Allow-Origin', origin)
  # response.headers.add('Access-Control-Allow-Headers', 'Cookie,Content-Type,Authorization, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
  response.headers.add('Access-Control-Allow-Headers','*')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
  response.headers.add('Access-Control-Allow-Credentials','true')
  response.headers.add('Allow-Origin-With-Credentials','true')
  del response.headers["Server"]


  return response

@app.errorhandler(sqlalchemy.exc.PendingRollbackError)
def restart_because_of_socket_error(my_event):
  print_if_dev(my_event.__class__)
  response = APIMsgFormat({},"There was an issue with the DB connection")
  my_resp = make_response(jsonify(response.__dict__))
  my_resp.status_code = 500
  return my_resp


@app.errorhandler(APIError)
def handle_api_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = APIMsgFormat({},err.description)
    if len(err.args) > 0:
        response.msg = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error( "{} : {}".format(err.description, response.msg ))
    my_resp = make_response(jsonify(APIError().__dict__))
    my_resp.status_code = err.code
    return my_resp


@app.errorhandler(500)
def handle_unknown_exception(err):
    """Return JSON instead of HTML for any other server error"""
    print(err)
    app.logger.error("Unknown Exception: {}".format(str(err)))
    # app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = APIMsgFormat({},"This is a server error please contact support if the issue persits")


    return response.return_flask_response(), 500

@app.teardown_appcontext
def app_shutdown(event):
  CONFIGS.cron_task_runner.stop_task()



app.add_url_rule('/', 'index', (lambda: "test 1"))

if __name__ == "__main__":
    if ENV_VARS.get("FLASK_BACKEND_ENV") == "DEV":

      # IMPORTANT: do not set this in run_backend_env this is a part of your
      # computers system env vars and you should set it seprately in an admin shell or CMD or powershell
      # ssl_cert = ENV_VARS.get("WML_CERT0","cert.pem")
      # ssl_key  = ENV_VARS.get("WML_CERT_KEY0","key.pem")

      # app.run(
      #   use_reloader=True,
      #   exclude_patterns="site-packages",
      #   debug=True,ssl_context=(ssl_cert,ssl_key),port=CONFIGS.app["backend_port"])
      app.run(
        use_reloader=True,
        exclude_patterns="site-packages",
        debug=True,port=CONFIGS.app["backend_port"])

    else:
      app.run()

