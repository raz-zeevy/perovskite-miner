import pandas as pd
import numpy as np


def load_data(db_path):
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
