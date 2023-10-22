from functools import wraps
from utils.api_exceptions import APIAuthenticationError
from utils.iterable_utils import flatten_list
from utils.local_deps import local_deps
from utils.print_if_dev import print_if_dev

local_deps()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import auth
from utils.singleton_exception import SingletonException
from utils.env_vars import flask_backend_env
from flask import request, jsonify


class FirebaseManager:
    init = False
    bucket = None
    env_vars = {}

    def __init__(self, env_vars) -> None:
        if self.init:
            raise SingletonException
        else:
            self.init = True
            self.env_vars = env_vars
            if flask_backend_env in ["DEV", "TEST"]:
                firebase_admin.initialize_app(
                    None,
                    {
                        "authDomain": "127.0.0.1",
                        "storageBucket": "tooboards-57f9c.appspot.com",
                    },
                )

            elif flask_backend_env in ["PREVIEW"]:
                self._connect_to_firebase_https(
                    "tooboards-57f9c.appspot.com", "tooboards-57f9c.firebaseapp.com"
                )
            elif flask_backend_env in ["PROD"]:
                self._connect_to_firebase_https(
                    "tooboards-prod.appspot.com", "tooboards-prod.appspot.com"
                )
            self.bucket = storage.bucket()
            self.auth = auth





    def _connect_to_firebase_https(self, storage_bucket, auth_domain):
        firebase_admin.initialize_app(
            options={"authDomain": auth_domain, "storageBucket": storage_bucket}
        )



    def _get_blob(self, topic, id, env=None):
        env = env if env else self.env_vars.get("FLASK_BACKEND_ENV")
        target_blob = "{}/{}/{}".format(env, topic, id)
        return self.bucket.list_blobs(prefix=target_blob)

    def get_images_related_to_products(self, product_ids):
        result = []
        for product_id in product_ids:
            blobs = self._get_blob(topic="products", id=product_id)
            objects = [blob.name for blob in blobs]
            file_objects = list(filter(lambda x: not x.endswith("/"), objects))
            result.append(file_objects)
        return result

    def delete_user(self, uid, retry=5):
        try:
            auth.delete_user(uid)
        except BaseException as e:
            if retry != 0:
                self.delete_user(uid, retry - 1)

    def list_users(self, uids=[], retry=5,filter_uids=True):
      all_users =[]
      page_obj = None
      def get_users(retry_0 =5):
        try:
          nonlocal page_obj
          page_obj = auth.list_users()
          all_users.append(page_obj.users)
        except BaseException as e:
          if retry_0 != 0:
            get_users(retry_0-1)
      get_users(retry)
      while page_obj.has_next_page:
        get_users(retry)
      all_users = flatten_list(all_users)
      if filter_uids == True:
        all_users = list(filter(lambda x:x.uid in uids,all_users))
      return all_users

    def set_env_for_user(self, uid):
        user = auth.get_user(uid)
        new_claims = user.custom_claims["env"] if user.custom_claims else []
        new_claims.append(flask_backend_env)
        auth.set_custom_user_claims(uid, {"env": list(set(new_claims))})
