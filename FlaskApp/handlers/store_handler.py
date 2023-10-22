from configs import CONFIGS
from google.api_core.rest_helpers import _flatten_list
from utils.iterable_utils import flatten_list
from utils.my_util import pull_unique_items_from_list
from utils.print_if_dev import print_if_dev
from utils.wml_libs.pagination import WMLAPIPaginationRequestModel, WMLAPIPaginationResponseModel


def list_products(page_data):
  product_info = CONFIGS.square_manager.list_products()
  res_data = []
  for x in product_info["objects"]:
    main_price = x["item_data"]["variations"][0]["item_variation_data"]["price_money"]
    square_price =  main_price
    options_obj, options_keys = _get_option_data_from_products(x)
    price = CONFIGS.square_manager.get_values_based_on_currency(
      square_price["amount"],
      square_price["currency"]
    )
    variations = []
    for variation in x["item_data"]["variations"]:
      variations.append({
        "id":variation["id"],
        "option_ids":[
          {
            "key":y["item_option"]["id"],
            "value":y["item_option_value"]["id"],
          } for y in variation["item_variation_data"]["item_option_values"]
        ]
      })

    product_item =  {
      "id":x["id"],
      "title":x["item_data"]["name"],
      "category":x["item_data"]["category_id"],
      "subtitle":x["item_data"]["description"],
      "price":price,
      "options":{
        "key":options_keys,
        "values":options_obj,
      },
      "variations":variations
    }
    res_data.append(product_item)
    for x in page_data.get("filter",[]):
      res_data =list(
          filter(
            lambda y :y[x["key"]] ==x["value"], res_data
          )
        )

  product_param_paths = CONFIGS.firebase_manager.get_images_related_to_products(
    [x["id"] for x in res_data ]
  )
  for index,x in enumerate(res_data):
    x["image_urls"] = product_param_paths[index]
  start_index= page_data["page_num"] * page_data["page_size"]
  end_index= (page_data["page_num"] + 1) * page_data["page_size"]

  res_page_object = WMLAPIPaginationResponseModel(data=res_data[start_index:end_index],page_num=page_data["page_num"])
  res_page_object.calculate_current_state(total_items=len(res_data),page_size =page_data["page_size"])
  return res_page_object

def list_categories(page_data):
  data = CONFIGS.square_manager.list_categories(page_data)
  data = [{"name":x["category_data"]["name"],"id":x["id"]} for x in data ]
  page_data =  WMLAPIPaginationResponseModel(
    data=data)
  data.insert(0, {"name":"Shop All","id":""} )
  page_data.calculate_current_state()
  return page_data

def purchase_products(req_body,square_uid):
  return {
    "payment_link":CONFIGS.square_manager.create_payment_link(
      req_body["cart_items"],
      square_uid
    )
  }

def list_lto_expirations():
  result_set = CONFIGS.postgres_manager.get_rows_from_table(
    WMLAPIPaginationRequestModel(
      page_size=1
    ),
    "Settings"
  )
  result_set.data = [
    {
      "expiration_date":x["expiration_date"]
    } for x in result_set.data
  ]
  return {
    "items":result_set.to_json()["data"]
  }

def _get_option_data_from_products(x):
    options = [y["item_variation_data"] for y in x["item_data"]["variations"]]
    options = flatten_list([y["item_option_values"] for y in options])
    options_obj ={}
    for option in options:
      option_key_name = option["item_option"]["name"]
      if not options_obj.get(option_key_name):
        options_obj[option_key_name] =[]
      options_obj[option_key_name].append(option["item_option_value"])
    for k,v in options_obj.items():
      options_obj[k] = pull_unique_items_from_list(v)
    options_keys   = pull_unique_items_from_list([y["item_option"] for y in options])
    return options_obj,options_keys
