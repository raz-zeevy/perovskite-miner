import requests
import json
import pandas as pd
import questions_const
from config import OPEN_AI_KEY
import openai

model_4 = 'gpt-3.5-turbo'
model_16 = 'gpt-3.5-turbo-16k'

def post_paper_prompt(p_prompts, fake=False):
    from prompt_engineering.prompt_engineering import PaperPrompt
    if not isinstance(p_prompts, PaperPrompt):
        raise "argument must be of type PaperPrompt"
    res = ''
    for i in range(p_prompts.number_of_api_calls):
        res += access_chat_gpt_3(p_prompts.contents[i],
                                 fake=fake)
    return res

def access_chat_gpt_3(prompts_text: [],
                      fake=False):
    if fake:
        return "DOI: 10.1016/j.jacc.2019.11.056\n" \
               "PMID: 31918846\n" \
               "Number of patients: 1,000\n" \
               "Patients age: 50-60\n"
    openai.api_key = OPEN_AI_KEY
    # list models
    # models = openai.Model.list()
    # print the first model's id
    # print(models.data[0].id)
    # create a chat completion
    prompts = [dict(role="user",
                    content=txt) for txt in prompts_text]
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=prompts)
    res = chat_completion.choices[0].message.content
    return res


if __name__ == '__main__':
    access_chat_gpt_3()
