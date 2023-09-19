from pandas import DataFrame
from gpt_api import post_paper_prompt
from prompt_engineering.prompt_engineering import PaperPrompt
import datetime
from data_exploration.utlis import *
import os
import json

def log_gpt_results_json(p_prompt: PaperPrompt, res, pdf_path,
                         accuracy, fields) -> None:
    def log_path(paper_pdf_path):
        split_name = paper_pdf_path.split(".")
        output = ".".join(split_name[:-1])
        return output + "_log.json"

    pdf_name = os.path.basename(pdf_path)

    # Create a dictionary for the log entry
    log_entry = {
        "Index": 'NA',
        "Date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Paper": pdf_name,
        "API Calls": p_prompt.number_of_api_calls,
        "Shrinking methods": p_prompt.shrink_method,
        "Questions count": len(p_prompt.questions),
        "Questions per API call": p_prompt.questions_per_api_call,
        "Tokens per API call": p_prompt.tokens_per_api_call,
        "Paper Length": p_prompt.paper_prompt_tokens,
        "Response Accuracy": f"{accuracy:.2f}%",
        "Prompt": p_prompt.contents[0][0],
        "Response": res,
        "Questions Fields": ', '.join(fields)
    }
    # Check if the log file already exists
    log_file_path = log_path(pdf_path)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_entry)
    logs[-1]["Index"] = len(logs)
    with open(log_file_path, 'w', encoding='utf-8') as file:
        json.dump(logs, file, indent=4)


def gpt_fill(paper_pdf_path, fields=None, questions=None, qids=None,
             fake=False) -> \
        DataFrame:
    q_df = load_questions_db()
    # filter data according to given filters
    q_df = q_df[q_df[FIELD_NAME].isin(get_kpi_fields())]
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
    log_gpt_results_json(p_prompts, res, paper_pdf_path, 0, q_df[FIELD_NAME].
                         values)
    # check if results are unsuccessful
    if ":" not in res:
        return res
    return results_to_df(res, columns=q_df[FIELD_NAME].to_list())


def results_to_df(res, columns: list):
    res = res.strip()
    res_rows = [row for row in res.split("\n") if row]
    api_cols = [value.split(":")[0] for value in res_rows]
    values = [value.split(":")[1] for value in res_rows]
    res_df = pd.DataFrame(columns=columns)
    # Create dictionaries for column names and values
    api_cols_dict = {columns[i]: api_cols[i] for i in range(len(api_cols))}
    values_dict = {columns[i]: values[i] for i in range(len(values))}
    # append rows
    res_df = res_df.append(api_cols_dict, ignore_index=True)
    res_df = res_df.append(values_dict, ignore_index=True)
    return res_df


def mine_paper(paper_pdf_path, fake=False):
    def output_name(paper_pdf_path):
        split_name = paper_pdf_path.split(".")
        output = ".".join(split_name[:-1])
        return output + "_api_results.csv"

    y_pred = gpt_fill(paper_pdf_path, fake=fake)
    if isinstance(y_pred, DataFrame):
        y_pred.to_csv(output_name(paper_pdf_path), index=False)


if __name__ == '__main__':
    paper_pdf_path = r"data/papers/downloads/10.1002_adem.201900288.pdf"
    mine_paper(paper_pdf_path, fake=True)
