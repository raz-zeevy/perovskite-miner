from pypdf import PdfReader
from typing import List
from .prompt_engineering_consts import preview_prompt, preview_prompt_tokens, tokens_deviation
from apis.gpt_api import openai_count_tokens
import math
import sys
sys.path.insert(0, '../data_exploration')


def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Could not open pdf file '{file_path}' due to: {str(e)}")
    return text


def clean_text(text):
    def trim_end(input_text: str, word: str):
        for word in [word.capitalize(), word, word.upper()]:
            index = input_text.rfind(word)
            if index != -1:
                return input_text[:index]
        return input_text

    out_text = trim_end(text, 'references')
    out_text = trim_end(out_text, 'acknowledgements')
    return out_text


def truncation(input_text, tokens_for_paper=15000, count_tokens=openai_count_tokens) -> str:
    """
    In this method we heuristically take the most tokens we can get from
    the begging of the paper that would fit in 3 API calls.
    We assume that token is about 0.75 of a word and deviate from the 'tokens_for_paper' by 100 tokens.
    :return: trimmed paper text.
    """
    words = input_text.split()
    words_amount = tokens_to_words_count(tokens_amount=tokens_for_paper)
    shortened_text = ' '.join(words[:words_amount])
    diff = count_tokens(shortened_text) - tokens_for_paper
    while abs(diff) > tokens_deviation:
        if count_tokens(shortened_text) > tokens_for_paper:
            words_amount -= tokens_to_words_count(tokens_deviation) // 2
        else:
            words_amount += tokens_to_words_count(tokens_deviation) // 2
        shortened_text = ' '.join(words[:words_amount])
        diff = count_tokens(shortened_text) - tokens_for_paper
    return shortened_text


def summarization(input_text, tokens_for_paper=15000) -> str:
    # todo: implement using OPENAI API. summarize paper, try to not lose
    #  experimental data.
    return input_text


def fragmentation(input_text, tokens_for_paper=15000) -> str:
    # todo: send only most relevant parts of the paper based on the questions.
    return input_text


def aggressive_trimming(input_text, tokens_for_paper=15000) -> str:
    # todo: using PDF parser remove sections based on where we think.
    return input_text


def tokens_to_words_count(tokens_amount: int):
    # todo: statistically check which constant is best for this function
    return int(tokens_amount * 0.55)


class PaperPrompt:
    """
    A class to represent a paper prompt which is used to generate prompts for a GPT model.

    Attributes
    ----------
    number_of_api_calls : int
        The number of API calls made (default is 1).
    contents : List[str]
        The content to be sent to the GPT model, a list in length of 'number_of_api_calls' where in each index we
        include the preview prompt, paper prompt, and questions prompt for one API call.
    questions_per_api_call: int, int
        The number of questions to be sent in each API call, and remainder questions to be sent in the last API call.
    tokens_per_api_call: List[int]
        The number of tokens in each API call.
    paper_prompt_tokens: int
        The number of tokens in the paper prompt inserted to the model.

    Methods
    -------
    __init__(self, paper_pdf_path: str, questions: List[str])
        Initializes the PaperPrompt object with the paper PDF path and a list of questions.
    """
    def __init__(self, paper_pdf_path: str, questions: List[str], max_tokens: int, answers_max_tokens: int,
                 max_api_calls: int = 10, preferred_shrink_method: str = 'truncation',
                 count_tokens=openai_count_tokens):
        """
        Initializes the PaperPrompt object with the paper PDF path and a list of questions.
        """
        self.contents = None
        self.number_of_api_calls = None
        self.questions_per_api_call = None
        self.tokens_per_api_call = []
        self.paper_prompt_tokens = None
        self.shrink_method = "None"

        self.max_tokens = max_tokens
        self.questions_tokens = count_tokens(" ".join(questions))
        self.answers_max_tokens = answers_max_tokens
        self.max_api_calls = max_api_calls
        self.chosen_shrink_method = preferred_shrink_method
        self.paper_prompt = clean_text(read_pdf(paper_pdf_path))
        self.questions = questions
        self.count_tokens = count_tokens
        self.generate_prompts()

    def generate_prompts(self):
        paper_tokens = self.count_tokens(self.paper_prompt)
        non_paper_needed_tokens = self.questions_tokens + self.answers_max_tokens + preview_prompt_tokens
        if paper_tokens > self.max_tokens:
            buffer_tokens = math.ceil(non_paper_needed_tokens / 3)
            self.number_of_api_calls = 3
            self.shrink_method = self.chosen_shrink_method
            self.paper_prompt = self.shrink(self.chosen_shrink_method, self.max_tokens - buffer_tokens)
        else:
            free_tokens = self.max_tokens - self.count_tokens(self.paper_prompt)
            self.number_of_api_calls = math.ceil(non_paper_needed_tokens / free_tokens)

            if self.number_of_api_calls > self.max_api_calls:
                raise Exception("Usage: Paper requires too many API calls.")
        self.paper_prompt_tokens = self.count_tokens(self.paper_prompt)
        questions_per_call = math.ceil(len(self.questions) / self.number_of_api_calls)
        self.questions_per_api_call = questions_per_call, len(self.questions) % questions_per_call

        self.contents = []
        for i in range(0, len(self.questions), questions_per_call):
            batch_questions = self.questions[i:i + questions_per_call]
            questions_prompt = " ".join(batch_questions)
            self.contents.append([preview_prompt, self.paper_prompt, questions_prompt])
            tokens_in_call = preview_prompt_tokens + self.paper_prompt_tokens + self.count_tokens(questions_prompt)
            self.tokens_per_api_call.append(tokens_in_call)

    def shrink(self, shrink_method: str, tokens_for_paper=15000) -> str:
        """
        Shrinks the paper text to fit the max tokens according to selected method.
        """
        if shrink_method == "truncation":
            return truncation(self.paper_prompt, tokens_for_paper)
        elif shrink_method == "summarization":
            return summarization(self.paper_prompt, tokens_for_paper)
        elif shrink_method == "fragmentation":
            return fragmentation(self.paper_prompt, tokens_for_paper)
        elif shrink_method == "aggressive_trimming":
            return aggressive_trimming(self.paper_prompt, tokens_for_paper)
        else:
            raise Exception("Usage: shrink method not supported, please choose one of the following: [truncation, " +
                            "summarization, fragmentation, aggressive_trimming]")

