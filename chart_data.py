
import pathlib
import pandas as pd
import os
import numpy as np



DATA_DIR = pathlib.Path(__file__).parent / "data"
OEMOF_SCENARIO = "2045_scenario"


def get_postprocessed_data():
    return pd.read_csv(DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "scalars.csv", delimiter=";")

def get_preprocessed_file_list():
    path = DATA_DIR / OEMOF_SCENARIO / "preprocessed" / "data" / "elements"
    print(path)
    file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
    filtered_file_list = [f for f in file_list if not any(x in f for x in ["commodity", "demand", "bus", "export", "import", "transmission"])]
    return filtered_file_list

def get_preprocessed_file_df():
    resultDf = pd.DataFrame()
    file_list = get_preprocessed_file_list()

    for file in  file_list:
        file_path = DATA_DIR / OEMOF_SCENARIO / "preprocessed" / "data" / "elements" / file
        techDf = pd.read_csv(file_path, delimiter=";")
        resultDf = pd.concat([resultDf, techDf], ignore_index=True)

    return resultDf
       

    

