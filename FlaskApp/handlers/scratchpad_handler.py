from configs import CONFIGS


def delete_all_users(data):
    target_env = "_"+data.get("env","dev")
    users = CONFIGS.firebase_manager.list_users(filter_uids=False)
    firebase_uids = [user.uid for user in users]
    CONFIGS.firebase_manager.auth.delete_users(firebase_uids)

    square_users = CONFIGS.square_manager.client.customers.list_customers(limit=100)
    for user in square_users.body.get("customers",[]):
      if target_env in user["reference_id"]:
        CONFIGS.square_manager.client.customers.delete_customer(
        customer_id = user["id"]
      )
