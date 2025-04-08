
import pathlib
import pandas as pd

DATA_DIR = pathlib.Path(__file__).parent / "data"
OEMOF_SCENARIO = "2045_scenario"


def get_postprocessed_data():
    return pd.read_csv(DATA_DIR / OEMOF_SCENARIO / "postprocessed" / "scalars.csv", delimiter=";")

