from typing import List, Tuple
import pandas as pd
from pandas import DataFrame
from questions_const import FIELD_NAME, PROTOCOL_QUESTION, QID, GPT_QUESTION
from gpt_api import access_chat_gpt_3


def generate_prompts(pdf_path: str, questions: List[str]) -> List[str]: pass


def gpt_fill(paper_pdf_path, fields=None, questions=None, qids=None) -> \
        DataFrame:
    questions_db_path = r"data/questions/questions_db.csv"
    q_df = pd.read_csv(questions_db_path)
    # filter data according to given filters
    q_df = q_df[q_df[FIELD_NAME].notna()]
    for filter, values in {FIELD_NAME: fields,
                           PROTOCOL_QUESTION: questions,
                           QID: qids}.items():
        if values:
            q_df = q_df[q_df[filter].isin(values)]
    # TODO: make the psuedo code work
    # prompts = generate_prompts(paper_pdf_path, q_df[GPT_QUESTION].values)
    p_prompts = PaperPrompt(paper_pdf_path, q_df[GPT_QUESTION].values)
    for i in range(p_prompts.num_of_api_calls):
        res = access_chat_gpt_3(p_prompts.contents[i])
    # Structure the results
    res = res.split("\n")
    res_df = pd.DataFrame(columns=q_df[FIELD_NAME].values)
    res_df.append(res, ignore_index=True)
    return res_df


if __name__ == '__main__':
    paper_pdf_path = r"data/paper1.pdf"
    paper_data_path = r"data/db_output1.pdf"
    y_pred = gpt_fill(paper_pdf_path)
