

def post_endpoint(req_data):
  return req_data


def receive_doc(data):
  file_data = data["resume"]["content"].encode()
  binary_data = base64.b64decode(file_data)
  my_buffer = BytesIO(binary_data)
