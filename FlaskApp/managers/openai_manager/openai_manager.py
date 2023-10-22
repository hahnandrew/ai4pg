import json
import re
from enum import Enum

from utils.print_if_dev import print_if_dev
from utils.singleton_exception import SingletonException



from utils.local_deps import local_deps
local_deps()
import openai
import sentry_sdk

class OpenAIModelCompletionEnum(Enum):
  BABBAGE = "babbage"
  ADA = "ada"
  CURIE = "curie"
  DAVINCI = "davinci"
  TEXT_DAVINCI_003={
    "name":"text-davinci-003",
    "max_tokens":4097
  }
class OpenAIModelChatCompletionEnum(Enum):
  GPT_35_TURBO_0301 ={
    "name":"gpt-3.5-turbo-0301",
    "max_tokens":4096
  }
  GPT_35_TURBO = {
    "name":"gpt-3.5-turbo",
    "max_tokens":4096
  }


class OpenAIManager():
  init= False
  client = None
  def __init__(self,api_key):
    if(self.init):
      raise SingletonException
    else:
      self.init = True
      openai.api_key = api_key

  def _ask_chatgpt(self,prompt,model,randomness=0,debug_via_sentry= False):
    prompt = re.sub(r"[\n\t\r\f]", "", prompt)
    response =""
    content ={}
    if(isinstance(model,OpenAIModelCompletionEnum)):
      response = openai.Completion.create(
        model=model.value["name"],
        prompt=prompt,
        temperature=randomness,
        max_tokens=model.value["max_tokens"]-len(prompt)
      )
      content = re.sub(r'[\\\n]', '', response.choices[0].text)
    else:
      response = openai.ChatCompletion.create(
          model=model.value,
          messages=[{
            "role":"user",
            "content":prompt,
          }],
          temperature=randomness,
      )

      content = re.sub(r'[\\\n]', '', response.choices[0].message.content)
    if debug_via_sentry:
      self._debug_with_sentry(content)
    return content

  def _debug_with_sentry(self,my_str_with_spaces):
    my_str =re.sub(r"[\n\t\r\f]", "", my_str_with_spaces)
    section_length = 950
    sections = len(my_str) // section_length
    for i in range(sections):
      if i == sections -1:
        sentry_sdk.capture_message(my_str[i*section_length:(len(my_str)-1)])
      else:
        sentry_sdk.capture_message(my_str[i*section_length:((i+1)*section_length)])

