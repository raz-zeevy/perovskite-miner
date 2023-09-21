import pandas as pd
import numpy as np
from data_exploration.questions_const import *


def filter_by_kpi(df: pd.DataFrame) -> None:
    kpi_fields = get_kpi_fields()
    for col in df.columns:
        if col not in kpi_fields:
            df.drop(columns=col, inplace=True)  # Select columns in-place


def get_kpi_fields():
    q_df = load_data('data/questions/questions_db.csv')
    keys = q_df[q_df[FIELD_NAME].notna()][FIELD_NAME].to_list()
    keys.remove("Ref_name_of_person_entering_the_data")
    keys.remove("Ref_data_entered_by_author")
    return keys


def load_data(db_path='../data/Perovskite_database_content_all_data.csv'):
    df = pd.read_csv(db_path, low_memory=False)
    df.replace("Unknown", np.nan, inplace=True)
    return df


# todo finish this function
def sample_disjoint_devices(df: pd.DataFrame, n=1):
    """
    Sample n random devices from the database that are taken from different
    devices.
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


def sample_paper_devices(df: pd.DataFrame,
                         min_num_of_of_devices=-np.inf,
                         max_num_of_of_devices=np.inf):
    """
    Sample a random paper from the database that has a certain number of
    references
    :param df:
    :param min_num_of_of_devices:
    :param max_num_of_of_devices:
    :return:
    """
    count_ref_df = df.groupby("Ref_DOI_number")['Ref_ID'].count()
    count_ref_df = count_ref_df[(count_ref_df >= min_num_of_of_devices) &
                                (count_ref_df <= max_num_of_of_devices)]
    random_doi = np.random.choice(count_ref_df.index)
    return df[df["Ref_DOI_number"] == random_doi]


def load_questions_db():
    questions_db_path = r"data/questions/questions_db.csv"
    try:
        return pd.read_csv(questions_db_path)
    except FileNotFoundError:
        return pd.read_csv("../"+questions_db_path)

if __name__ == '__main__':
    a = load_data('../data/db_output1.csv')
    filter_by_kpi(a)
