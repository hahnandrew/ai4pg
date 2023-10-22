

import base64
from io import BytesIO

from configs import CONFIGS


def post_endpoint(req_data):
  return req_data


def receive_doc(data):
  file_data = data["resume"]["content"].encode()
  binary_data = base64.b64decode(file_data)
  my_buffer = BytesIO(binary_data)
  resume_text = CONFIGS.document_manager.extract_text_from_resume(my_buffer,data["resume"]["type"])
  print(resume_text)
