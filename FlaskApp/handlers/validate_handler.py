

import base64
from io import BytesIO
import mimetypes

from configs import CONFIGS


def receive_doc(binary_data):
  # file_data = data.encode()
  # uploaded_file = data
  # file_data = uploaded_file.encode()
  # binary_data = base64.b64decode(data)

  base64_data = base64.b64encode(binary_data)
  base64_string = base64_data.decode('utf-8')
  # my_buffer = BytesIO(base64_string)
  my_buffer = BytesIO(binary_data)
  resume_text = CONFIGS.document_manager.extract_text_from_resume(my_buffer,"application/pdf")
  print(resume_text)
