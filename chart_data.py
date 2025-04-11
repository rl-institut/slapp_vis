
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

def get_postprocessed_sequences_bus_time(): 
    path = DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "sequences" / "bus"
    file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    data = pd.Series()

    for file_name in file_list:
        df = pd.read_csv(path / file_name, sep=';')
        for col_name in df.columns:
            cell_name = df.iloc[0][col_name]
            
            if 'electricity-demand' in cell_name:
                column_sum = df.loc[2:, col_name].astype(float).sum()

                parts = file_name.split('-')
                region = parts[0]

                data[region] = column_sum    

    return data

def get_postprocessed_by_variable_flow(filename = "flow.csv"):
    path = DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "sequences" / "by_variable" / filename
    df = pd.read_csv(path, sep=';',skiprows=3, header=None, index_col=0)
    return df





   
        
       

    

