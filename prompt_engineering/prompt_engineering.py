import sys

sys.path.insert(0, '../data_exploration')

from pypdf import PdfReader
import tiktoken
import os
import pandas as pd
from typing import List
from prompt_engineering_consts import gpt_preview_prompt
import math


def count_tokens(input_text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_count = len(encoding.encode(input_text))
    return token_count


def calculate_mean(token_counts):
    if token_counts:
        return sum(token_counts) / len(token_counts)
    else:
        return 0


def calculate_std(token_counts):
    if not token_counts:
        return 0

    mean = calculate_mean(token_counts)
    variance = sum((x - mean) ** 2 for x in token_counts) / len(token_counts)
    std_dev = math.sqrt(variance)
    return std_dev


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def clean_pdf_text(text):
    out_text = text
    for word in ['References', 'references', 'References'.upper()]:
        index = text.rfind(word)
        if index != -1:
            out_text = text[:index]
            break

    for word in ['acknowledgements', 'acknowledgements'.upper(), 'Acknowledgements']:
        index = text.rfind(word)
        if index != -1:
            out_text = text[:index]
            break

    return out_text


def create_text_from_questions_table():
    questions_pd = pd.read_csv('../data/questions/questions_db.csv')
    questions_pd = questions_pd[questions_pd['field_name'].notna()]['gpt_question']
    print(len(questions_pd))
    questions_output = ''
    for row in questions_pd.values:
        questions_output += row
        questions_output += ','
    return questions_output[:-1]


class PaperPrompt:
    """
    A class to represent a paper prompt which is used to generate prompts for a GPT model.

    Attributes
    ----------
    number_of_api_calls : int
        The number of API calls made (default is 1).
    content_to_gpt : List[str]
        The content to be sent to the GPT model, a list in length of 'number_of_api_calls' where in each index we
        include the preview prompt, paper prompt, and questions prompt for one API call.

    Methods
    -------
    __init__(self, paper_pdf_path: str, questions: List[str])
        Initializes the PaperPrompt object with the paper PDF path and a list of questions.
    """

    # constants for q&a tokens

    # add file prompt analysis

    def __init__(self, paper_pdf_path: str, questions: List[str], max_tokens: int):
        """
        Initializes the PaperPrompt object with the paper PDF path and a list of questions.
        """
        self.contents = None
        self.number_of_api_calls = None
        self.paper_prompt = clean_pdf_text(read_pdf(paper_pdf_path))
        self.questions = questions
        self.generate_prompts()

    def generate_prompts(self):
        paper_tokens = count_tokens(self.paper_prompt)
        if paper_tokens <= 13000:
            self.number_of_api_calls = 1
            questions_prompt = ','.join(self.questions)
            self.contents = [[gpt_preview_prompt, self.paper_prompt, questions_prompt]]
        elif paper_tokens <= 15000:
            questions_middle = len(self.questions) / 2
            first_questions_prompt = ','.join(self.questions[questions_middle:])
            second_questions_prompt = ','.join(self.questions[:questions_middle])
            self.number_of_api_calls = 2
            self.contents = [[gpt_preview_prompt, self.paper_prompt, first_questions_prompt],
                                   [gpt_preview_prompt, self.paper_prompt, second_questions_prompt]]
        else:
            print("Paper is more then 15000 tokens")
            # todo: handle files that are greater then 15k tokens.
            raise "todo"


def rows_to_strings(df):
    return df.apply(lambda row: ' '.join(row.astype(str)), axis=1)


def main(directory_path):
    token_counts = []
    clean_token_count = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    text = read_pdf(file_path)
                    token_counts.append(count_tokens(text))
                    clean_text = clean_pdf_text(text)
                    clean_token_count.append(count_tokens(clean_text))
                except Exception as e:
                    print(f"Could not read file '{file}' due to: {str(e)}")

    mean_token_count = calculate_mean(token_counts)
    mean_clean_token_count = calculate_mean(clean_token_count)

    std_token_count = calculate_std(token_counts)
    std_clean_token_count = calculate_std(clean_token_count)

    print(f"The mean number of tokens across all PDFs is: {mean_token_count}")
    print(f"The mean number of tokens across all clean PDFs is: {mean_clean_token_count}")
    print(f"The standard deviation of tokens across all PDFs is: {std_token_count}")
    print(f"The standard deviation of tokens across all clean PDFs is: {std_clean_token_count}")
