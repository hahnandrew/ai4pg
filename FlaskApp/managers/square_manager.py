
import json
import math
import os
import random
import time
import uuid
from utils.iterable_utils import flatten_list, list_get
from utils.print_if_dev import print_if_dev
from utils.api_exceptions import APIClientError, APIServerError
from utils.singleton_exception import SingletonException
from utils.local_deps import  local_deps
from utils.wml_libs.pagination import WMLAPIPaginationResponseModel
from utils.env_vars import flask_backend_env
local_deps()
from square.client import Client

class SquareManager():
  init= False
  client = None
  online_location_id =None
  CONFIGS = None
  def __init__(self,access_token,location_name,CONFIGS):
    if flask_backend_env == "TEST":
      return 
    if(self.init):
      raise SingletonException
    else:
      self.init = True
      self.client = Client(
        access_token=access_token,
        environment='sandbox' if flask_backend_env != "PROD" else "production",
        max_retries=2,
        timeout=10
      )
      self.online_location_id = self._get_location_id(location_name)
      self.CONFIGS = CONFIGS

  def _combine_items_and_options(self,items,options):
    extracted_options = []
    extracted_values = []
    self._create_option_mapping(options, extracted_options, extracted_values)
    self._assign_option_data_to_items(items, extracted_options, extracted_values)
    return items

  def _create_option_mapping(self, options, extracted_options, extracted_values):
      for option in options["objects"]:
        extracted_options.append({
        "id":option["id"],
        "name":option["item_option_data"]["name"]
      })
        for x in option["item_option_data"]["values"]:
          extracted_values.append({
          "id":x["id"],
          "name":x["item_option_value_data"]["name"]
        })

  def _assign_option_data_to_items(self, items, extracted_options, extracted_values):
    for product in items["objects"]:
      for variation in product["item_data"]["variations"]:
        for option in variation["item_variation_data"]["item_option_values"]:
          option["item_option"] = list(
            filter(
              lambda x:option["item_option_id"] == x["id"],extracted_options
            )
          )[0]
          option["item_option_value"] = list(
            filter(
              lambda x:option["item_option_value_id"] == x["id"],extracted_values
            )
          )[0]
          del option["item_option_id"]
          del option["item_option_value_id"]

  def _get_location_id(self,location_name):
    result = self.client.locations.list_locations()
    if result.is_success():
      my_id = next((x["id"] for x in result.body["locations"] if x["business_name"] ==location_name),None)
      return my_id
    elif result.is_error():
      raise APIServerError(result.errors)

  def _check_if_all_api_calls_completed_sucessfully(self, results):
      all_success = all(result["success"] == True for result in results)
      if not all_success:
        raise APIServerError(
        list(
          map(lambda x:x["result"].errors,
            filter(lambda x: x["fail"] == True,  results))
        )
      )

  def _update_results_list(self,results,result):
      results.append({
        "result":result,
        "success":result.is_success(),
        "fail":result.is_error()
      })

  def get_product_by_id(self,object_id):
    result = self.client.catalog.retrieve_catalog_object(
      object_id
    )
    if result.is_success():
      return result.body
    elif result.is_error():
      return result.errors

  def _check_if_user_exists(self,reference_id,retry=5):
    try:
      duplicates = self.client.customers.search_customers(
        body = {
          "query": {
            "filter": {
              "reference_id": {
                "exact": reference_id
              }
            }
          }
        }
      )
      if duplicates.is_success():
        return  duplicates
      if duplicates.is_error():
        raise APIServerError("Error while trying to check for duplicates")
    except BaseException as e:
      if retry != 0:
        self._check_if_user_exists(reference_id,retry-1)

  def create_reference_id(self,firebase_uid):
    return "{}_{}".format(firebase_uid,flask_backend_env.lower())

  def list_products(self):
    items = self.client.catalog.list_catalog(
      types = "ITEM"
    )
    options = self.client.catalog.list_catalog(
      types = "ITEM_OPTION"
    )
    items.body["objects"] = list(
      filter(
        lambda x: self.online_location_id in x.get("present_at_location_ids",[]),
        items.body["objects"]))

    if items.is_success() and options.is_success() :
      return self._combine_items_and_options(items.body,options.body)
    else:
      raise APIServerError({
        items:items.errors,
        options:items.errors
      })

  def get_values_based_on_currency(self,value,currency="USD"):

    currency_info= {
      "USD":{
        "display":"${}".format("{:.2f}".format(round(value / 100, 2))),
        "business":"{:.2f}".format(round(value / 100, 2)),
        "currency":"$"
      }
    }[currency]
    return currency_info

  def transform_currency_to_square_values(self,value,currency="USD"):
    currency_info= {
      "USD":lambda x:math.ceil(x*100)
    }[currency]
    return currency_info(value)

  def create_payment_link(self,cart_items,customer_id=None):
    my_checkout_body = {
        "order": {
          "location_id": self.online_location_id,
          "line_items": cart_items
        }
      }
    if customer_id != None:
      my_checkout_body["order"]["customer_id"] = customer_id
    my_checkout = self.client.checkout.create_payment_link(
      body = my_checkout_body
    )
    if my_checkout.is_success():
      my_updated_checkout = self.client.checkout.update_payment_link(
        id = my_checkout.body["payment_link"]["id"],
        body = {
          "payment_link": {
            "version":1,
            "checkout_options": {
              "allow_tipping": True,
              "redirect_url": "{}{}{}".format(
                self.CONFIGS.app["frontend_angular_app_url"],
                "/store/order-confirmed?orderId=",
                my_checkout.body["payment_link"]["order_id"]
              )
            }
          }
        }
      )
      if my_updated_checkout.is_success():
        return my_checkout.body["payment_link"]["long_url"]
      elif my_updated_checkout.is_error():
        raise  APIServerError(my_updated_checkout.errors)
    elif my_checkout.is_error():
      raise APIServerError(my_checkout.errors)

  def update_catalog_variation_item(self,object_id,price=0.00,reset=False):
    variations = self.get_product_by_id(object_id)["object"]["item_data"]["variations"]
    square_variation_data = []

    for x in variations:

      item_variation_data = x["item_variation_data"]
      if reset == True:
        item_variation_data["location_overrides"] =[]
      else:
        item_variation_data["location_overrides"] =[
          {
            "location_id":self.online_location_id,
            "price_money":{
              "amount":self.transform_currency_to_square_values(price),
              "currency": item_variation_data["price_money"]["currency"]
            }
          }
        ]


      variation_body ={
        "type": "ITEM_VARIATION",
        "id": x["id"],
        "version": x["version"],
        "is_deleted": False,
        "present_at_all_locations": True,
        "item_variation_data":item_variation_data
      }
      square_variation_data.append(variation_body)

    update_value = str(uuid.uuid4())
    result = self.client.catalog.batch_upsert_catalog_objects(
      body = {
        "idempotency_key":update_value,
        "batches":[
          {
            "objects":square_variation_data
          }
        ],
      }
    )


    if result.is_error():
      APIServerError(result.errors)

  def get_customer_via_firebase_id(self,firebase_id):
    reference_id = self.create_reference_id(firebase_id)

    result = self.client.customers.search_customers(
      body = {
        "query": {
          "filter": {
            "reference_id": {
              "exact": reference_id
            }
          }
        }
      }
    )

    if result.is_success():
      print_if_dev(result.body,True)
      customers = result.body.get("customers",{})
      if len(customers) > 1:
        self.CONFIGS.sentry_manager.debug_with_sentry(
            "Customer with firebase_id {} has {} customer ids".format(
            firebase_id,
            [item["id"] for item in result.body["customers"]]
          )
        )
      return customers[0]
    elif result.is_error():
      raise APIServerError(result.errors)

  def create_customer(self,firebase_uid,email):
    reference_id = self.create_reference_id(firebase_uid)
    duplicates = self._check_if_user_exists(reference_id)
    if   duplicates.body.get("customers",None) != None:
      return {"customer":duplicates.body["customers"][0]}

    body = {
      "given_name":reference_id,
      "email_address":email,
      "idempotency_key": reference_id,
      "reference_id": reference_id,
    }
    result = self.client.customers.create_customer(body)
    if result.is_success():
      return result.body
    if result.is_error():
      raise APIServerError(result.errors)

  def update_customers(self,req_body):
    results = []
    for customer in req_body:
      result = self.client.customers.update_customer(
        customer_id = customer["id"],
        body = {
          "address":customer["address"]
        }
      )
      self._update_results_list(results,result)
    self._check_if_all_api_calls_completed_sucessfully(results)

  def list_customers(self):
    results = []
    while True:
      result = self.client.customers.list_customers()
      self._update_results_list(results,result)
      self._check_if_all_api_calls_completed_sucessfully(results)
      if result.body.get("cursor",None) is  None:
        break
    ret_val =[]
    for result in results:

      ret_val.append(result["result"].body.get("customers",[]))
    ret_val = flatten_list(ret_val)
    return ret_val

  def get_customer(self,pagination_dict):
    body = {
      "query": {
        "filter": {}
      }
    }
    reference_id =list_get(
      list(filter(lambda x:x["key"] == "reference_id",  pagination_dict["filter"])),
      0,None
    )
    if reference_id != None:
      body["query"]["filter"]["reference_id"] = {
        "exact": reference_id['value']
      }
    result = self.client.customers.search_customers(
      body
    )

    if result.is_success():
      data = result.body.get("customers",[])
      page_data =  WMLAPIPaginationResponseModel(
        data=data,
        page_num=pagination_dict["page_num"],
        page_size=pagination_dict["page_size"])
      page_data.calculate_current_state()
      return page_data
    elif result.is_error():
      raise APIServerError(result.errors)

  def delete_customers(self,square_customer_ids):
    results = []
    for my_id in square_customer_ids:
      result = self.client.customers.delete_customer(
        customer_id = my_id
      )
      self._update_results_list(results,result)

    self._check_if_all_api_calls_completed_sucessfully(results)

  def store_customer_card_on_file(self,customer_id,payment_method_token):

    too_big = self.list_cards_via_customer_id([customer_id])
    if len(list_get(too_big.data,0,[])) >= 8:
      return APIServerError("TOO_MANY_CARDS")
    result = self.client.cards.create_card(
      body = {
        "idempotency_key": str(uuid.uuid4()),
        "source_id": payment_method_token,
        "card": {
          "customer_id": customer_id
        }
      }
    )

    if result.is_success():
      None
    elif result.is_error():
       raise APIServerError(result.errors)

  def list_cards_via_customer_id(self,ids):
    results = []
    for my_id in ids:
      result = self.client.cards.list_cards(
        customer_id =my_id
      )
      self._update_results_list(results,result)

    self._check_if_all_api_calls_completed_sucessfully(results)

    res_page_data = []
    for result in results:
      data = result["result"].body.get("cards",[])
      res_page_data.append([{
        "enabled":x["enabled"],
        "exp_month":x["exp_month"],
        "exp_year":x["exp_year"],
        "last_4":x["last_4"],
        "card_brand":x["card_brand"],
        "id":x["id"]
      } for x in data])
    page_data =  WMLAPIPaginationResponseModel(data=res_page_data)
    page_data.calculate_current_state()
    return page_data

  def delete_cards(self,card_ids,customer_id):
    customer_cards_page_res_model = self.list_cards_via_customer_id([customer_id])
    results =[]
    for customer_card in customer_cards_page_res_model.data:
      for card_id in card_ids:
        result = list(filter(lambda x:x["id"] == card_id,customer_card))
        if len(result) > 0:
          result = self.client.cards.disable_card(
            card_id = card_id
          )
        self._update_results_list(results,result)


      self._check_if_all_api_calls_completed_sucessfully(results)

  def list_categories(self,pagination_dict):
    body = {
      "query": {
        "filter": {}
      }
    }
    result = self.client.catalog.list_catalog(
      types = "CATEGORY"
    )

    if result.is_success():
      data = result.body.get("objects",[])
      return data
    elif result.is_error():
      raise APIServerError(result.errors)

