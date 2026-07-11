import pandas as pd

def transform_data(data):
    df = pd.json_normalize(data)
    df.drop_duplicates(inplace=True)
    return df