
import json
import pathlib
import string
import inspect
import sys
import pandas as pd


import chart_data

DIST_DIR = pathlib.Path(__file__).parent / "dist"
TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"


def render_chart(template: str, data: list[dict[str, float]]):
    with (TEMPLATE_DIR / template).open("r", encoding="utf-8") as f:
        html_template = f.read()
    html_rendered = string.Template(html_template).substitute(data=json.dumps(data))
    with (DIST_DIR / template).open("w", encoding="utf-8") as f:
        f.write(html_rendered)


def total_electricity_per_technology():
    template = "total_electricity_per_technology.html"
    scalars = chart_data.get_postprocessed_data()
    filtered = scalars[(scalars["var_name"] == "flow_out_electricity") & (scalars["var_value"] > 0)][["name", "var_value"]]
    filtered.columns = ["name", "value"]
    filtered["value"] = (filtered["value"] / filtered["value"].sum() * 100).round()
    return template, filtered.to_dict(orient="records")

def electricity_import():
    template = "electricity_import.html"
    scalars = chart_data.get_postprocessed_data()
    import_df = scalars[(scalars["var_name"] == "flow_out_electricity") & (scalars["tech"] == "import") & (scalars["var_value"] > 0)][["name", "var_value"]]
    export_df = scalars[
        (scalars["var_name"] == "flow_in_electricity") & (scalars["tech"] == "export") & (scalars["var_value"] > 0)][
        ["name", "var_value"]]
    result = [import_df["var_value"].sum(), -export_df["var_value"].sum()]
    return template, result

def optimized_capacities():
    template = "optimized_capacities.html"
    
    file_list = chart_data.get_preprocessed_file_list()
    file_names_list = [file_name[:-4] for file_name in file_list]

    scalars_df = chart_data.get_postprocessed_data()

    var_value_df = scalars_df[(scalars_df['var_name'].str.contains('invest_out|invest_in')) &
                        (scalars_df['name'].str.contains('|'.join(file_names_list)) ) 
                       ]


    capacity_potential_df = chart_data.get_preprocessed_file_df()

    merged_df = pd.merge(var_value_df, capacity_potential_df, on='name', how='outer')
    merged_df = merged_df[['name', 'var_value', 'capacity_potential', 'var_name']]




    merged_df.loc[merged_df['capacity_potential'] == float('inf'), 'capacity_potential'] = 0
    merged_df.loc[merged_df['capacity_potential'] == float('-inf'), 'capacity_potential'] = 0

    merged_df = merged_df[(merged_df['var_value'].notna()) & 
                          (merged_df['capacity_potential'].notna() &
                           merged_df['capacity_potential'] > 0)
                          ]

    return template, merged_df.to_dict(orient="records")

def generation_consumption_per_sector():
    template = "generation_consumption_per_sector.html"
    scalars = chart_data.get_postprocessed_data()

    y1 = scalars[(scalars["var_name"] == "flow_out_electricity")]['var_value'].sum()
    x1 = scalars[(scalars["var_name"] == "flow_in_electricity")]['var_value'].sum()

   

    y2 = scalars[(scalars["var_name"] == "flow_out_heat_low_decentral")]['var_value'].sum()
    x2 = scalars[(scalars["var_name"] == "flow_in_heat_low_decentral")]['var_value'].sum()

    y3 = scalars[(scalars["var_name"] == "flow_out_heat_low_central")]['var_value'].sum()
    x3 = scalars[(scalars["var_name"] == "flow_in_heat_low_central")]['var_value'].sum()

    y4 = scalars[(scalars["var_name"] == "flow_out_heat_high")]['var_value'].sum()
    x4 = scalars[(scalars["var_name"] == "flow_in_heat_high")]['var_value'].sum()

    data = {
        "chart1-1": x1,
        "chart1-2": y1 - x1,
        "chart1-total": round(y1, 2),

        "chart2-1": y2,
        "chart2-2": x2 - y2,
        "chart2-total": round(y2, 2),

        "chart3-1": y3,
        "chart3-2": x3 - y3,
        "chart3-total": round(y3, 2),

        "chart4-1": y4,
        "chart4-2": x4 - y4,
        "chart4-total": round(y4, 2),
    }
    return template, data

def self_generation_imports():
    template = "self_generation_power.html"
    scalars = chart_data.get_postprocessed_data()
    y1_df = scalars[(scalars['var_name'] == 'flow_out_electricity') & (~scalars['type'].isin(['shortage', 'storage']))]
    y1 = y1_df['var_value'].sum()

    y2_df = scalars[(scalars['var_name'] == 'flow_out_electricity') & (scalars['tech'] == 'import')]
    y2 = y2_df['var_value'].sum()
    
    data = {
        "y1": y1,
        "y2": y2,
        "x": round(y1 + y2, 2),
    }
    return template, data

def supplied_hours():
    template = "supplied_hours.html"
    y1 = chart_data.get_postprocessed_sequences_bus_time()
    y2 = 8760 - y1
    x = y1 + y2

    y1 = y1 / x * 100
    y2 = y2 / x * 100

    data = pd.DataFrame()
    data['y1'] = y1.round(2)
    data['y2'] = y2.round(2)

    print(data.to_dict())

    return template, data.to_dict()

def interactive_time_series_plot():
    template = "interactive_time_series_plot.html"
    data_df = pd.DataFrame()
    flow_df = chart_data.get_postprocessed_by_variable_flow("flow.csv")
    storage_content_df = chart_data.get_postprocessed_by_variable_flow("storage_content.csv")

    data_df['flow zeit 1'] = flow_df[1]
    data_df['storage content zeit 1'] = storage_content_df[1]

    data_df['flow zeit N'] = flow_df[2]
    data_df['storage content zeit N'] = storage_content_df[3]
    return template, data_df.to_dict()


if __name__ == "__main__":
    functions_list = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for f_name, fct in functions_list:
        if f_name == "render_chart":
            continue
        _template, _data = fct()
        render_chart(_template, _data)

