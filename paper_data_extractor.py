import time
from pandas import DataFrame
from apis.gpt_api import post_paper_prompt
from prompt_engineering.prompt_engineering import PaperPrompt
from evaluate.fields_matching import match_api_output
import datetime
from data.utils import *
import os
import json
import re

RESULTS_DIR = "results/"


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
        "Paper Length (tokens)": p_prompt.paper_prompt_tokens,
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
                            preferred_shrink_method="truncation",
                            max_api_calls=10)
    if fake:
        from data.utils import mock_response
        res = mock_response(q_df[FIELD_NAME].values, n_missing_fields=7)
    else:
        res = post_paper_prompt(p_prompts, fake=fake)
    log_gpt_results_json(p_prompts, res, paper_pdf_path, 0, q_df[FIELD_NAME].
                         values)
    # check if results are unsuccessful
    if ":" not in res:
        return res
    return results_to_df(res, kpi_fields=q_df[FIELD_NAME].to_list())


def results_to_df(res, kpi_fields: list):
    res = res.strip()
    res_rows = [row for row in res.split("\n") if row]
    # matching fields and values
    api_fields = [value.split(":")[0] for value in res_rows]
    values = [value.split(":")[1] for value in res_rows]
    api_output = {api_fields[i] : values[i] for i in range(len(api_fields))}
    matched_fields, matched_values = match_api_output(kpi_fields, api_output)
    # append rows
    res_df = pd.DataFrame(columns=kpi_fields)
    res_df = res_df.append(matched_fields, ignore_index=True)
    res_df = res_df.append(matched_values, ignore_index=True)
    return res_df

  
#  todo: should split to 2 functions: one that extracts the data and another that saves it to a csv file.
def mine_paper(paper_pdf_path, fake=False):
    def output_name(paper_pdf_path):
        split_name = re.split(r'[./]', paper_pdf_path)
        pdf_name = split_name[-2]
        if not os.path.exists(RESULTS_DIR):
            os.makedirs(RESULTS_DIR)
        return RESULTS_DIR + pdf_name + "_api_results.csv"

    y_pred = gpt_fill(paper_pdf_path, fake=fake)
    if isinstance(y_pred, DataFrame):
        y_pred = pd.DataFrame(np.vstack([y_pred.columns, y_pred])).T
        y_pred.columns = ['Field name', 'AI question', 'AI answer']
        y_pred.to_csv(output_name(paper_pdf_path), index=False)
    return y_pred


def mine_paper_by_doi(paper_doi, fake=True):
    from scraper.utils import sanitize
    download_folder = "dataset/papers/downloads"
    pdf_name = sanitize(paper_doi) + ".pdf"
    pdf_path = os.path.join(download_folder, pdf_name)
    return mine_paper(pdf_path, fake=fake)


def create_results_vs_db_output(results_df, paper_doi, fake=False):
    """
    Create a csv file that contains the results of the GPT-3 API and the
    database side by side.
    :param fake:
    :param results_df: the results of the GPT-3 API.
    :param paper_doi: paper DOI number.
    """
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    all_data = load_perovskite_data()
    paper_row = all_data[all_data['Ref_DOI_number'] == paper_doi]
    paper_row = paper_row[get_kpi_fields()]

    df1 = results_df.iloc[:1]
    df2 = results_df.iloc[1:]

    # Concatenate the DataFrames with the paper_row in between
    results_df = pd.concat([df1, paper_row, df2], ignore_index=True)
    results_df = pd.DataFrame(np.vstack([results_df.columns, results_df])).T
    results_df.columns = ["db_field_name","ai_field_name", "db_answer",
                          "ai_answer"]
    output_name = RESULTS_FOLDER + f"/{sanitize(paper_doi)}_combined_results.csv"
    if fake:
        output_name = output_name.replace("combined", "combined_fake")
    results_df.to_csv(output_name, index=False)


if __name__ == '__main__':
    for paper_doi in ['10.1557/adv.2019.79', '10.1016/j.ces.2019.01.003', '10.1021/acs.nanolett.6b02158',
                      '10.1016/j.jpowsour.2015.05.106', '10.1016/j.solmat.2016.07.037']:
        try:
            fake = False
            start_time = time.time()
            df_result = mine_paper_by_doi(paper_doi, fake=fake)
            create_results_vs_db_output(df_result, paper_doi, fake=fake)
            print(f"saved combined results for paper {paper_doi} - "
                  f"{round((time.time()-start_time)/60,2)} min")
            # filter_non_boolean_questions()
        except Exception as e:
            print(f"Parse Failed: for paper:{paper_doi}" + str(e))
            raise e

