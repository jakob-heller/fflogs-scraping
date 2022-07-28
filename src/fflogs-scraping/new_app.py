"""Nerv nicht."""

import re
import data.combination as dc
import pandas as pd
from dash import Dash, html, dcc
from dash.dash_table import DataTable as DT
from dash.dependencies import Input, Output, State


def main():
    """Nerv nicht."""

    print("Combining data...", flush=True, end=" ")
    df_lists = dc.csv_to_dfs()
    dmg = dc.join_dd_dfs(df_lists[0])
    heal = dc.join_hd_dfs(df_lists[1])
    print("...combination finished.", flush=True)

    dash(dmg, heal).run_server(debug=True, port=8051)


def dash(dfr1: pd.DataFrame, dfr2: pd.DataFrame) -> Dash():
    """Creates an interactive Dashboard with 2 sortable tables.

    The style.css in the assets directory sets the dashboards
    background color and the properties of the html.H2 object.

    Args:
      dfr1:
        Pandas dataframe of summarized damage done.
      dfr2:
        Pandas dataframe of summarized healing done.

    Returns:
      Object of Dash class which can then be run on localhost.
    """
    app = Dash(__name__)
    tbl1 = dfr_to_dt(dfr1, "tbl1")
    tbl2 = dfr_to_dt(dfr2, "tbl2")
    layout(app, tbl1, tbl2)

    return app


def layout(app: Dash, tbl1: DT, tbl2: DT) -> Dash():
    """Creates the layout of the dash application."""
    app.layout = html.Div([
        html.Div([
            html.Div([
                DT(
                    id='adding-rows-table',
                    columns=[{
                        'name': 'URLs',
                        'id': 'url-column'
                    }],
                    data=[],
                    editable=True,
                    row_deletable=True,
                    style_as_list_view=True,
                    style_cell=(table_styles("cell") | {'textAlign': 'left'}),
                    style_header=(table_styles("header") | {'textAlign': 'left'}),
                    style_data=table_styles("table_data"),
                    style_data_conditional=[                
                        {
                            "if": {"state": "selected"},
                            "color": "inherit",              # 'active' | 'selected'
                            "backgroundColor": "inherit",
                            "border": "1px solid #bb592c",
                            'textAlign': 'left'
                        },
                    ]
                ),
                html.Div([
                    dcc.Input(
                        id="inpt",
                        type="url",
                        placeholder="Input Log URL",
                        debounce=True,
                        name="Please enter a valid log URL.",
                        size="40",
                        style=table_styles("table_data")
                    ),
                    html.Div(id="output")
                ], id="styled-input", style={"width": "30%"}),
            ], style={'width': '30% 520px', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    ["All Encounters", "Kills only", "Wipes only"],
                    "All Encounters",
                    clearable=False,
                    style=table_styles("table_data")
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
        ]),
        html.Div([
            html.H2("Damage Done"),
            tbl1,
            html.H2("Healing Done"),
            tbl2,
        ])
    ], style={"backgroundColor": "#161a1d", "padding": 40})

    @app.callback(
        Output('adding-rows-table', 'data'),
        Output('inpt','value'),
        Output("output", "children"),
        Input("inpt", "value"),
        State('adding-rows-table', 'data'),
        State('adding-rows-table', 'columns'))
    def add_url_row(value, rows, columns):
        pattern = r"https:\/\/www.fflogs.com\/reports\/(a:)?[a-zA-Z0-9]{16}(\/*)?"
        invalid = ""
        if value is not None:
            if re.match(pattern, value):
                rows.append({c['id']: value for c in columns})
                value = ""
            else:
                invalid = "The URL needs to be a valid log."
        return (rows, value, invalid)

def dfr_to_dt(dfr: pd.DataFrame, table_id: str) -> DT:
    """Converts dataframe into DataTable, using previously defined styles."""
    r_column = "rDPS" if "rDPS" in dfr.columns else "rHPS"
    return DT(dfr.to_dict("records"),
              [{"name": i, "id": i, "selectable": True} for i in dfr.columns],
              id=table_id,
              sort_action="native",
              style_as_list_view=True,
              style_cell=table_styles("cell"),
              style_header=table_styles("header"),
              style_data=table_styles("table_data"),
              style_data_conditional=(
                  data_bars(dfr, "Amount Total") +
                  data_bars(dfr, r_column) +
                  parse_colors()),
              style_cell_conditional=column_width(dfr)
              )


# The following 4 methods are all only relevant for the dashboards style.

def table_styles(part: str) -> dict:
    """Returns dictionary of styles as specified by "part"."""
    if part == "header":
        return {
            "backgroundColor": "#0e1012",
            "color": "white"
        }
    elif part == "table_data":
        return {
                "backgroundColor": "#161a1d",
                "color": "white"
        }
    elif part == "cell":
        return {
            "font_size": "18px",
            "border": "1px solid #3f3f3f"
        }


def data_bars(dfr: pd.DataFrame, column: str) -> dict:
    """Conditional formatting for data bars in cells.

    Creates a conditional formatting dictionary that shows data bars inside of
    (data-)table cells. Bar lengths are relative to the highest value.

    .. note::
        This method was taken from the `official dash documentation
        <https://dash.plotly.com/datatable/conditional-formatting>`_ and
        slightly adjusted.

    Args:
      dfr:
        The pandas dataframe in question.
      column:
        The name of the column where bars are shown.

    Returns:
      A dictionary of conditional formatting that can be used to style a
      dash DataTable.
    """
    bar_color = "#f4d44d" if "DPS" in dfr.columns else "#91dfd2"
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((dfr[column].max() - dfr[column].min()) * i) + dfr[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 90
        styles.append({
            "if": {
                "filter_query": (
                    f"{{{column}}} >= {min_bound}" +
                    (f" && {{{column}}} < {max_bound}" if (i < len(bounds) - 1) else "")
                ),
                "column_id": column
            },
            "background": (
                f"""
                    linear-gradient(90deg,
                    {bar_color} 0%,
                    {bar_color} {max_bound_percentage}%,
                    #242a44 {max_bound_percentage}%,
                    #242a44 100%
                """
            ),
            "paddingBottom": 2,
            "paddingTop": 2
        })
    return styles


def column_width(dfr: pd.DataFrame) -> dict:
    """Returns conditional formatting dictionary for column widths."""
    styles = [
        {"if": {"column_id": "Parse %"},
         "width": "5%"},
        {"if": {"column_id": "Player Name"},
         "width": "10%"},
        {"if": {"column_id": "Amount %"},
         "width": "5%"},
        {"if": {"column_id": "Active %"},
         "width": "5%"},
        {"if": {"column_id": "DPS"},
         "width": "5%"},
        {"if": {"column_id": "rDPS"},
         "width": "15%"},
        {"if": {"column_id": "HPS"},
         "width": "5%"},
        {"if": {"column_id": "rHPS"},
         "width": "15%"},
        {"if": {"column_id": "Overheal"},
         "width": "5%"}
    ]
    # The healing table has one column more, We make "amount" smaller there.
    if "HPS" in dfr.columns:
        styles.append({"if": {"column_id": "Amount Total"}, "width": "45%"})
    else:
        styles.append({"if": {"column_id": "Amount Total"}, "width": "50%"})
    return styles


def parse_colors() -> dict:
    """Conditional formatting for parse colors.

    Creates a conditional formatting dictionary that changes the colors of
    values in the "Parse %" column dependend on their value.
    I am used to seeing those colors on the original website, that's why we
    implement them here aswell.

    Args:
      df:
        The pandas dataframe in question.

    Returns:
      A dictionary of conditional formatting that can be used to style a
      dash DataTable.
    """
    styles = [
        {
            "if": {
                "filter_query": "{Parse %} < 25",
                "column_id": "Parse %"
            },
            "color": "#666",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} > 24 && {Parse %} < 50",
                "column_id": "Parse %"
            },
            "color": "#1bb607",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} > 49 && {Parse %} < 75",
                "column_id": "Parse %"
            },
            "color": "#035fb9",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} > 74 && {Parse %} < 95",
                "column_id": "Parse %"
            },
            "color": "#822dbc",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} > 94 && {Parse %} < 99",
                "column_id": "Parse %"
            },
            "color": "#ff8000",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} = 99",
                "column_id": "Parse %"
            },
            "color": "#db7ea7",
            "fontWeight": "bold"
        },
        {
            "if": {
                "filter_query": "{Parse %} = 100",
                "column_id": "Parse %"
            },
            "color": "#b29f65",
            "fontWeight": "bold"
        },
    ]
    return styles


if __name__ == "__main__":
    main()
