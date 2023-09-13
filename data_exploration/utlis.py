import pandas as pd
import numpy as np
def load_data(db_path):
    df = pd.read_csv(db_path, low_memory=False)
    df.replace("Unknown", np.nan, inplace=True)
    return df