from typing import List, Tuple
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
import const
from gpt_api import access_chat_gpt_3


def generate_prompts(pdf_path: str, questions: List[str]) -> List[str]: pass


def gpt_fill(paper_pdf_path, fields=None, questions=None, qids=None) -> \
        DataFrame:
    questions_db_path = r"data/questions/questions_db.csv"
    q_df = pd.read_csv(questions_db_path)
    # filter data according to given filters
    q_df = q_df[q_df[const.FIELD_NAME].notna()]
    for filter, values in {const.FIELD_NAME: fields,
                           const.PROTOCOL_QUESTION: questions,
                           const.QID: qids}.items():
        if values:
            q_df = q_df[q_df[filter].isin(values)]
    prompts = generate_prompts(paper_pdf_path, q_df[const.GPT_QUESTION].values)
    res = access_chat_gpt_3(prompts)
    # Structure the results
    res = res.split("\n")
    res_df = pd.DataFrame(columns=q_df[const.FIELD_NAME].values)
    res_df.append(res, ignore_index=True)
    return res_df


if __name__ == '__main__':
    paper_pdf_path = r"data/paper1.pdf"
    paper_data_path = r"data/db_output1.pdf"
    y_pred = gpt_fill(paper_pdf_path)
