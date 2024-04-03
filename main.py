import os
import sys
import ast
from langchain.schema import HumanMessage, ChatMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from functionsImplementations import get_all_teams

import constants
import functionsDescriptions

os.environ["OPENAI_API_KEY"] = constants.APIKEY
model = ChatOpenAI(model="gpt-4")

user_request = sys.argv[1]

def function_call(function_name, arguments):
    if function_name in globals() and callable(globals()[function_name]):
        function = globals()[function_name]
        result = function(*arguments)
        return result
    else:
        raise ValueError(f"The function {function_name} does not exist")
    
def get_dictionary_values(dictionarystring):
    dictionary = ast.literal_eval(dictionarystring)
    values = []
    for value in dictionary.values():
        values.append(str(value))
    return values

first_message = model.predict_messages(
    [HumanMessage(content=user_request)],
    functions=functionsDescriptions.desc
)

if not first_message.additional_kwargs:
  print(first_message)
  print('@DEVLOG@ --> no api calls')
  exit()

function_name = first_message.additional_kwargs["function_call"]["name"]
arguments = first_message.additional_kwargs["function_call"]["arguments"]

firstCallResults = function_call(function_name, get_dictionary_values(arguments))

second_message = model.predict_messages(
    [
      HumanMessage(content=user_request),
      ChatMessage(
        role='function',
        additional_kwargs = {'name': function_name},
        content = str(firstCallResults)
      )
    ],
    functions=functionsDescriptions.desc
)

print(second_message)