import numpy as np
import pandas as pd
from pandas import DataFrame
from gpt_api import post_paper_prompt
from prompt_engineering.prompt_engineering import PaperPrompt
import datetime
from data_exploration.utlis import *

LOG_ROW_LENGTH = 80


def log_gpt_results(p_prompt: PaperPrompt, res, pdf_path,
                    accuracy, fields) -> None:
    def log_path(paper_pdf_path):
        split_name = paper_pdf_path.split(".")
        output = ".".join(split_name[:-1])
        return output + "_res.log"

    pdf_name = pdf_path.split("\\")[-1].split(".")[0]
    log = f"Date: [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
    log += f"Paper: {pdf_name}\n"
    log += f"API Calls: {p_prompt.number_of_api_calls}\n"
    log += f"Shrinking methods: {p_prompt.shrink_method}\n"
    log += f"Questions count: {len(p_prompt.questions)}\n"
    log += f"Questions per API call: {p_prompt.questions_per_api_call}\n"
    log += f"Tokens per API call: {p_prompt.tokens_per_api_call}\n"
    log += f"Prompt Length: {p_prompt.paper_prompt_tokens} tokens\n"
    log += f"Response Accuracy: {accuracy:.2f}%\n"
    log += "-" * LOG_ROW_LENGTH + "\n"
    log += f"Prompt: \n{p_prompt.contents[0]}\n"
    log += "-" * LOG_ROW_LENGTH + "\n"
    log += f"Response: \n{res}\n"
    log += "-" * LOG_ROW_LENGTH + "\n"
    log += f"Fields: {', '.join(fields)}\n"
    log += ("=" * LOG_ROW_LENGTH + "\n") * 2

    with open(log_path(paper_pdf_path), "a", encoding='utf-8') as output:
        output.write(log)


def gpt_fill(paper_pdf_path, fields=None, questions=None, qids=None,
             fake=False) -> \
        DataFrame:
    # todo write in people who insert the model name and remove this question
    q_df = load_questions_db()
    # filter data according to given filters
    q_df = q_df[q_df[FIELD_NAME].notna()]
    for filter, values in {FIELD_NAME: fields,
                           PROTOCOL_QUESTION: questions,
                           QID: qids}.items():
        if values:
            q_df = q_df[q_df[filter].isin(values)]
    p_prompts = PaperPrompt(paper_pdf_path=paper_pdf_path,
                            questions=q_df[GPT_QUESTION].values,
                            max_tokens=int(1.6e4),
                            answers_max_tokens=500,
                            shrink_method="truncation",
                            max_api_calls=10)
    res = post_paper_prompt(p_prompts, fake=fake)
    log_gpt_results(p_prompts, res, paper_pdf_path, 0, q_df[FIELD_NAME].
                    values)
    # check if results are unsuccessful
    if ":" not in res:
        return res
    return results_to_df(res, columns=q_df[FIELD_NAME])


def results_to_df(res, columns):
    api_cols = [value.split(":")[0] for value in res.split("\n")]
    values = [value.split(":")[1] for value in res.split("\n")]
    res_df = pd.DataFrame(columns=columns)
    res_df.append(api_cols, ignore_index=True)
    res_df.append(values, ignore_index=True)
    return res_df


def mine_paper(paper_pdf_path):
    def output_name(paper_pdf_path):
        split_name = paper_pdf_path.split(".")
        output = ".".join(split_name[:-1])
        return output + "_api_results.csv"

    y_pred = gpt_fill(paper_pdf_path, fake=True)
    if isinstance(y_pred, DataFrame):
        y_pred.to_csv(output_name(paper_pdf_path))


if __name__ == '__main__':
    paper_pdf_path = r"data/papers/downloads/10.1002_adem.201900288.pdf"
    y_pred = mine_paper(paper_pdf_path)
