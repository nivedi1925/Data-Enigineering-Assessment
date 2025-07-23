import pandas as pd
import json

__all__ = ['extract_json']

def extract_json(path):
    """ Ingest data from JSON
    Parameters:
        path : path to the directory file where JSON file strored
    Return:
        Return tuple containing Pandas datafrome objects
    """
    with open(path, encoding='utf-8') as f:
        data = json.loads(f.read())

    for index, obj in enumerate(data):
        obj['property_id'] = index + 1

    df = pd.json_normalize(data)

    df_HOA = pd.json_normalize(data, record_path='HOA', meta=["property_id"])
    df_Rehab = pd.json_normalize(data, record_path='Rehab',  meta=["property_id"])
    df_Valuation = pd.json_normalize(data, record_path='Valuation',  meta=["property_id"])

    return (df, df_HOA, df_Rehab, df_Valuation)
