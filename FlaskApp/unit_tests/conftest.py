from functools import wraps
import os
import tempfile
from managers.firebase_manager import check_for_authentication



def fake_check_for_authentication(optional=False,square_id_required=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if square_id_required == True:
                return func("firebase_id","square_id", *args, **kwargs)
            else:
                return func("firebase_id", *args, **kwargs)
        return wrapper
    return decorator


check_for_authentication.check_for_authentication = fake_check_for_authentication

from app import app
import requests

import pytest

@pytest.fixture
def app_test():

    app.config.update(
      TESTING= True,
    )

    # before each


    yield app

    # after each



@pytest.fixture
def client(app_test):
    return app_test.test_client()


@pytest.fixture
def runner(app_test):
    return app_test.test_cli_runner()


@pytest.fixture
def auth(client):
    return client


class MyPlugin:
    def pytest_sessionfinish(self):
        print("\n*** test run reporting finishing")


class TestUtils:
    generic_fake_result ="result"

    @staticmethod
    def generic_fake(*args):
        return TestUtils.generic_fake_result

    @staticmethod
    def fake_jsonify(*args):
        return args[0]
