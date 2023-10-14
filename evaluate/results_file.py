import os
import time
from data.utils import load_perovskite_data, get_kpi_fields, sanitize
import numpy as np
import pandas as pd
from paper_data_extractor import mine_paper

RESULTS_FOLDER = r"db_vs_model_output"

def mine_paper_by_doi(paper_doi, fake=True):
    from data.utils import sanitize
    download_folder = "../dataset/papers/downloads"
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

    # Transpose the results_df and modify it for concatenating
    results_df = results_df.T
    results_df.columns = results_df.iloc[0]

    paper_row = all_data[all_data['Ref_DOI_number'] == paper_doi]
    paper_row = paper_row[get_kpi_fields()]

    db_field_names = results_df.iloc[:1]
    ai_fields_and_results = results_df.iloc[1:]

    # Concatenate the DataFrames with the paper_row in between
    results_df = pd.concat([db_field_names, paper_row,
                            ai_fields_and_results], ignore_index=True).T
    results_df.columns = ["db_field_name","db_answer", "ai_field_name",
                          "ai_answer"]
    output_name = RESULTS_FOLDER + f"/{sanitize(paper_doi)}_combined_results.csv"
    if fake:
        output_name = output_name.replace("combined", "combined_fake")
    results_df.to_csv(output_name, index=False)


if __name__ == '__main__':
    for paper_doi in [
        # '10.1557/adv.2019.79',
        # '10.1016/j.ces.2019.01.003',
        '10.1021/acs.nanolett.6b02158',
        '10.1016/j.jpowsour.2015.05.106',
        '10.1016/j.solmat.2016.07.037']:
        try:
            fake = False
            start_time = time.time()
            df_result = mine_paper_by_doi(paper_doi, fake=fake)
            all_data = load_perovskite_data()
            create_results_vs_db_output(df_result, paper_doi, fake=fake)
            print(f"saved combined results for paper {paper_doi} - "
                  f"{round((time.time()-start_time)/60,2)} min")
            # filter_non_boolean_questions()
        except Exception as e:
            print(f"Parse Failed: for paper:{paper_doi}" + str(e))
            raise e