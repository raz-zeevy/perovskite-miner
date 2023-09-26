import pandas as pd
import numpy as np
import math
from data.questions_const import *
from scraper.utils import sanitize
import os

QUESTIONS_DB_CSV = r"dataset/questions/questions_db.csv"


def filter_by_kpi(df: pd.DataFrame) -> None:
    kpi_fields = get_kpi_fields()
    for col in df.columns:
        if col not in kpi_fields:
            df.drop(columns=col, inplace=True)  # Select columns in-place


def get_kpi_fields():
    q_df = load_perovskite_data(QUESTIONS_DB_CSV)
    keys = q_df[q_df[FIELD_NAME].notna()][FIELD_NAME].to_list()
    keys.remove("Ref_name_of_person_entering_the_data")
    keys.remove("Ref_data_entered_by_author")
    return keys


def load_perovskite_data(db_path='dataset/Perovskite_database_content_all_data.csv'):
    try:
        df = pd.read_csv(db_path, low_memory=False)
    except FileNotFoundError:
        df = pd.read_csv('../' + db_path, low_memory=False)
    df.replace("Unknown", np.nan, inplace=True)
    return df


# todo finish this function
def sample_disjoint_devices(df: pd.DataFrame, n=1):
    """
    Sample n random entries (devices) from the database that are taken from
    different papers.
    :param df:
    :param n:
    :return:
    """
    dois = np.random.choice(df['Ref_DOI_number'].unique(), size=n,
                            replace=False)
    indices = []
    for doi in dois:
        indices.append(np.random.choice(df[df['Ref_DOI_number'] == doi].index))
    return df.loc[indices]


def sample_paper_by_devices(df: pd.DataFrame = None,
                            n=1,
                            min_num_of_of_devices=-np.inf,
                            max_num_of_of_devices=np.inf,
                            filter_by_available=False):
    """
    Sample a random paper from the database that has a certain number of
    references (devices)
    :param df:
    :param n:
    :param min_num_of_of_devices:
    :param max_num_of_of_devices:
    :param filter_by_available:
    :return:
    """
    if df is None :
        df = load_perovskite_data()
    if filter_by_available:
        df = filter_by_available_papers(df)
    count_ref_df = df.groupby("Ref_DOI_number")['Ref_ID'].count()
    count_ref_df = count_ref_df[(count_ref_df >= min_num_of_of_devices) &
                                (count_ref_df <= max_num_of_of_devices)]
    random_doi = np.random.choice(count_ref_df.index, size=n)
    return df[df["Ref_DOI_number"].isin(random_doi)]


def filter_by_available_papers(df: pd.DataFrame):
    papers_folder = "dataset/papers"
    papers = os.listdir(papers_folder)

    papers = [paper[:-4] for paper in papers]
    df = df[df['Ref_DOI_number'].apply(lambda x: sanitize(str(x))).isin(papers)]
    return df


def load_questions_db():
    questions_db_path = QUESTIONS_DB_CSV
    try:
        return pd.read_csv(questions_db_path)
    except FileNotFoundError:
        return pd.read_csv("../" + questions_db_path)


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


if __name__ == '__main__':
    a = load_perovskite_data('../data/db_output1.csv')
    filter_by_kpi(a)
