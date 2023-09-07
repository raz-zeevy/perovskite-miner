import openai

openai.api_key = "MY KEY"

gpt_logs = []
PREPROMPT = "you are an expert in chemistry and want to get data from a certain article into a perovskite database, \
  from each paper you want to extract properties of solar cells based on the article"


def start_conversation(task):
    gpt_logs.append({'role': 'user', 'content': PREPROMPT})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=gpt_logs
    )
    reply = response["choices"][0]["message"]["content"]
    i = reply.find("User:")
    if i != -1:
        reply = reply[:i]
    gpt_logs.append({'role': 'assistant', 'content': reply})
    return reply


def ask_gpt(question):
    """
    Ask a question to GPT-3 using OpenAI API.

    Args:
    - question (str): The question you want to ask GPT-3.

    Returns:
    - str: GPT-3's response.
    """


    response = openai.Completion.create(
        engine="davinci",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()


if __name__ == "__main__":
    user_question = input("Ask GPT-3: ")
    answer = ask_gpt(user_question)
    print(f"GPT-3 says: {answer}")