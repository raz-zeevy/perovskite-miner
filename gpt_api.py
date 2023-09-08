import requests
import json
from config import OPEN_AI_KEY

def access_chat_gpt():
    # Define the API endpoint
    endpoint = "https://api.openai.com/v1/engines/davinci/completions"
    # endpoint = "https://api.openai.com/v1/chat/completions"
    # Your OpenAI API key
    api_key = OPEN_AI_KEY
    # Set up headers
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python'
    }

    # Define your prompt and other parameters
    data = {
        "prompt": "Translate the following English text to French: 'Hello, how are you?'",
        "max_tokens": 150,
    }
    # Send the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    # Parse the response
    result = response.json()
    completion = result['choices'][0]['text'].strip()
    print(completion)
def access_chat_gpt_3():
    import openai
    openai.api_key = OPEN_AI_KEY
    # list models
    models = openai.Model.list()
    # print the first model's id
    print(models.data[0].id)
    # create a chat completion
    msg = dict(
        role="user",
        content="What is the capital of France?",
    )
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[msg])
    # print the chat completion
    print(chat_completion.choices[0].message.content)
def load_questions_from_txt(questions_path):
    questions = []
    with open(questions_path, "r") as questions_path:
        for line in questions_path:
            questions.append(line.strip())
    return questions

if __name__ == '__main__':
    questions_path = 'questions_5_4.txt'
    # load questions from txt file
    questions = load_questions_from_txt(questions_path)
    # access_chat_gpt_3()