import requests
import json
import pandas as pd
import questions_const
from config import OPEN_AI_KEY
import openai

def access_chat_gpt_3(prompts_text : []):
    openai.api_key = OPEN_AI_KEY
    # list models
    # models = openai.Model.list()
    # print the first model's id
    # print(models.data[0].id)
    # create a chat completion
    prompts = [dict(role = "user", content=txt) for txt in prompts_text]
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts)
    res = chat_completion.choices[0].message.content
    return res

if __name__ == '__main__':
    access_chat_gpt_3()