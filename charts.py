
import json
import pathlib
import string

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



if __name__ == "__main__":
    _template, _data = electricity_import()
    render_chart(_template, _data)

