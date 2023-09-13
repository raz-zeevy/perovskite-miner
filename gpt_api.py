import requests
import json
import pandas as pd
import const
from config import OPEN_AI_KEY
import openai

def access_chat_gpt_3(paper_prompt, question_prompt):
    openai.api_key = OPEN_AI_KEY
    # list models
    # models = openai.Model.list()
    # print the first model's id
    # print(models.data[0].id)
    # create a chat completion
    paper_prompt = dict(
        role="user",
        content="What is the capital of France?",
    )
    questions_prompt = dict(
        role="user",
        content="What is the capital of France?",
    )
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[paper_prompt, questions_prompt])
    res = chat_completion.choices[0].message.content
    return res

if __name__ == '__main__':
    access_chat_gpt_3()