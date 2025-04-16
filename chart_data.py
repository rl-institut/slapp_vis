import pathlib
import pandas as pd
import os


DATA_DIR = pathlib.Path(__file__).parent / "data"
OEMOF_SCENARIO = "2045_scenario"


def get_postprocessed_data():
    return pd.read_csv(
        DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "scalars.csv", delimiter=";"
    )


def get_preprocessed_file_list():
    path = DATA_DIR / OEMOF_SCENARIO / "preprocessed" / "data" / "elements"
    file_list = [f for f in os.listdir(path) if f.endswith(".csv")]
    filtered_file_list = [
        f
        for f in file_list
        if not any(
            x in f
            for x in ["commodity", "demand", "bus", "export", "import", "transmission"]
        )
    ]
    return filtered_file_list


def get_preprocessed_file_df():
    resultDf = pd.DataFrame()
    file_list = get_preprocessed_file_list()

    for file in file_list:
        file_path = (
            DATA_DIR / OEMOF_SCENARIO / "preprocessed" / "data" / "elements" / file
        )
        techDf = pd.read_csv(file_path, delimiter=";")
        resultDf = pd.concat([resultDf, techDf], ignore_index=True)

    return resultDf


def get_electricity_sequences():
    path = DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "sequences" / "bus"
    file_list = [f for f in os.listdir(path) if f.endswith(".csv") and "electricity" in f]

    data = []

    for file_name in file_list:
        df = pd.read_csv(path / file_name, index_col=0, header=None, sep=";")
        columns = df.iloc[:2].values
        df = df.iloc[3:]
        df.columns = list("|".join(item) for item in zip(columns[0], columns[1]))
        # This gives me strange output ? Look at timeindex around 8700 and you will see artifacts
        data.append(df)

    merged_df = pd.concat(data, axis=1)
    merged_df = merged_df.astype(float)
    return merged_df


def get_postprocessed_by_variable_flow(filename="flow.csv"):
    path = (
        DATA_DIR
        / OEMOF_SCENARIO
        / "postprocessed"
        / "sequences"
        / "by_variable"
        / filename
    )
    df = pd.read_csv(path, sep=";", skiprows=3, header=None, index_col=0)
    return df
