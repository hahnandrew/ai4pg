def flatten_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

def list_get(target_list,index,fallback_value={}):
  try:
    return target_list[index]
  except IndexError:
    return fallback_value
