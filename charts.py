
import json
import pathlib
import string
import shutil
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
        (scalars["var_name"] == "flow_out_electricity") & (scalars["tech"] == "export") & (scalars["var_value"] > 0)][
        ["name", "var_value"]]
    result = [import_df["var_value"].sum(), -export_df["var_value"].sum()]
    return template, result

def optimized_capacities():
    template = "optimized_capacities.html"
    
    file_list = chart_data.get_preprocessed_file_list()
    file_names_list = [file_name[:-4] for file_name in file_list]

    scalars_df = chart_data.get_postprocessed_data()

    var_value_df = scalars_df[(scalars_df['var_name'].str.contains('invest_out|invest_in|invest')) &
                        (scalars_df['name'].str.contains('|'.join(file_names_list)) ) 
                       ]

    capacity_potential_df = chart_data.get_preprocessed_file_df()

    merged_df = pd.merge(var_value_df, capacity_potential_df, on='name', how='outer')
    merged_df = merged_df[['name', 'var_value', 'capacity_potential']]

    print(var_value_df[var_value_df['name']== 'B-ch4-boiler_large'])


    merged_df.loc[merged_df['capacity_potential'] == float('inf'), 'capacity_potential'] = 0
    merged_df.loc[merged_df['capacity_potential'] == float('-inf'), 'capacity_potential'] = 0

    merged_df = merged_df[(merged_df['var_value'].notna()) & 
                          (merged_df['capacity_potential'].notna() &
                           merged_df['capacity_potential'] > 0)
                          ]
    return template, merged_df.to_dict(orient="records")



if __name__ == "__main__":
    _template, _data = optimized_capacities()
    shutil.copyfile(TEMPLATE_DIR / _template, DIST_DIR / _template)
    render_chart(_template, _data)

