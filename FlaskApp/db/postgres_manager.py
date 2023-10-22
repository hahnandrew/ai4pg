
import math
import os
import time
from utils.api_exceptions import APIError, APIServerError
from utils.print_if_dev import print_if_dev
from utils.singleton_exception import SingletonException
from utils.local_deps import  local_deps
from utils.specific.hash_string import hash_string
from utils.wml_libs.pagination import WMLAPIPaginationRequestModel, WMLAPIPaginationResponseModel
local_deps()
from sqlalchemy.engine.create import create_engine
from sqlalchemy import text
from datetime import datetime, timezone

import sqlalchemy


class PostgresManager():
  init= False
  current_conn_string = None
  sqlalchemy_0_engine = ""
  sqlalchemy_0_conn = ""
  CONFIGS = None


  def __init__(self,conn_string,CONFIGS):
    if(self.init):
      raise SingletonException
    else:
      self.init = True
      self.set_up_sql_conn(conn_string)
      self.CONFIGS = CONFIGS

  def set_up_sql_conn(self,conn_string,conn_obj={}):
      self.current_conn_string = conn_string
      if not conn_string:

        conn_string = "postgresql://{}:{}@{}:{}/{}".format(
          conn_obj.get("user"),
          conn_obj.get("pass"),
          conn_obj.get("host"),
          conn_obj.get("port"),
          conn_obj.get("db")
        )


      self.sqlalchemy_0_engine = create_engine(conn_string,pool_pre_ping=True)
      self.sqlalchemy_0_conn = self.sqlalchemy_0_engine.connect()


  @staticmethod
  def guard_against_conn_issues():
    error_counter = 7
    def decorator(func):
      def wrapper(self,*args, **kwargs):
        nonlocal error_counter
        error_counter -=1

        def handle_error(e):
          nonlocal error_counter
          if(error_counter != 0):
            return wrapper(self,*args, **kwargs)
          else:
            error_counter = 7
            raise e
        try:
            return func(self,*args, **kwargs)
        except sqlalchemy.exc.PendingRollbackError as e:
            self.sqlalchemy_0_conn.rollback()
            return handle_error(e)
        except sqlalchemy.exc.IntegrityError as e:
            self.sqlalchemy_0_conn.rollback()
            raise APIServerError(str(e))
        except sqlalchemy.exc.InternalError as e:
            self.sqlalchemy_0_conn.commit()
            return handle_error(e)
        except (
          AttributeError,
          sqlalchemy.exc.OperationalError
        ) as e:
            return handle_error(e)

      return wrapper
    return decorator




  @guard_against_conn_issues()
  def get_rows_from_table(self,
            pagination_req_obj = WMLAPIPaginationRequestModel(page_size=1),
            target_table=None):
    pagination_req_obj = pagination_req_obj.to_json()
    my_filter = pagination_req_obj.get("filter")
    my_sort = pagination_req_obj.get("sort")
    my_pageNum = pagination_req_obj.get("page_num")
    my_pageSize = pagination_req_obj.get("page_size")
    query = """
      SELECT *
      FROM {}
    """.format(target_table)
    total_items_query ="""
      SELECT count(*)
      FROM {}
    """.format(target_table)
    params ={
      # "target_table":target_table
    }
    if len(my_filter) != 0:
      params["filterKey"] = my_filter[0].get("key")
      params["filterValue"] = my_filter[0].get("value")
      query += ' WHERE {} LIKE :filterValue '.format(params["filterKey"])
      total_items_query += ' WHERE {} LIKE :filterValue '.format(params["filterKey"])
    if len(my_sort)!= 0:
      params["sortOn"] = my_sort[0].get("key")
      params["sortDirection"] = my_sort[0].get("direction")
      query += ' ORDER BY {} :sortDirection'.format(params["sortOn"])
    if isinstance(my_pageNum, (int)) and isinstance(my_pageSize, (int)):
      query += ' LIMIT  :pageSize OFFSET :offset'
      params["pageSize"] = my_pageSize
      params["offset"] = my_pageSize * my_pageNum
    query +=";"
    stmt = text(query)
    result_set = self.sqlalchemy_0_conn.execute(stmt,params)
    result_rows = [self.turn_row_to_dict(row) for row in result_set]
    total_items_stmt = text(total_items_query)
    total_items_result_set= self.sqlalchemy_0_conn.execute(total_items_stmt,params)
    total_items = total_items_result_set.scalar()
    page_size = len(result_rows)
    total_pages =  float(total_items) / float(my_pageSize)
    total_pages= math.ceil(total_pages)

    return WMLAPIPaginationResponseModel(
      data = result_rows,
      page_num = my_pageNum,
      page_size = page_size,
      total_pages = total_pages,
      total_items = total_items,
    )


  def turn_row_to_dict(self,row):
    row_dict = {}
    for k,v in row._mapping.items():
      if isinstance(v,bytes):
        row_dict[k] = str(v)
      else:

        row_dict[k] = v
        # for a previous version tbd
    # row_dict = dict(row._mapping)
    return row_dict

  def convert_value_to_timestamp_w_timezone(self, expiration_date):
      datetime_object = datetime.fromisoformat(expiration_date)
      desired_timezone = timezone.utc
      datetime_object = datetime_object.astimezone(desired_timezone)
      formatted_datetime = datetime_object.strftime("%Y-%m-%d %H:%M:%S.%f%z")
      return formatted_datetime


