
from utils.api_exceptions import APIClientError
from utils.singleton_exception import SingletonException
from utils.local_deps import local_deps
local_deps()
from pypdf import PdfReader
from docx2python import docx2python
import PyPDF2



class DocumentManager():
  init= False
  def __init__(self):
    if(self.init):
      raise SingletonException
    else:
      self.init = True

  def _extract_text_from_docx(self,bytesio_object):
    docx_content = docx2python(bytesio_object)

    docx_content.close()
    return docx_content.text



  def _extract_text_from_pdf(self,bytesio_object):
    pdf = PdfReader(bytesio_object)

    # resume_text = "".join([x.extract_text() for x in pdf.pages]) if len(pdf.pages) > 1 else pdf.pages[0].extract_text()

    resume_text = pdf.pages[0].extract_text()
    return resume_text

  def _extract_text_from_pdf2(self,bytesio_object):
    pdf_reader = PyPDF2.PdfReader(bytesio_object)
    text = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text.append(page.extract_text())
    return text


  def extract_text_from_resume(self,bytesio_object,file_type):

    if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return  self._extract_text_from_docx(bytesio_object)
    elif file_type == 'application/pdf':
        return  self._extract_text_from_pdf(bytesio_object)
    else:
        raise APIClientError
