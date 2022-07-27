"""Interactively visualize data using a basic Dash data app.

`Dash <https://dash.plotly.com/>`_ is a framework for rapidly building data
apps in Python (and other languages). It is built on top of Plotly.

The Dashboard is built by first converting the two dataframes to Dash
datatables. We then define the layout of our Dash app and return it.
There also are multiple methods returning "style dictionaries" that
are used as parameters to customize parts of the Dash dashboard.
"""

import pandas as pd
from dash import Dash, html
from dash.dash_table import DataTable as DT


def dash(df1: pd.DataFrame, df2: pd.DataFrame) -> Dash():
    """Creates an interactive Dashboard with 2 sortable tables.

    The style.css in the assets directory sets the dashboards
    background color and the properties of the html.H2 object.

    Args:
      df1:
        Pandas dataframe of summarized damage done.
      df2:
        Pandas dataframe of summarized healing done.

    Returns:
      Object of Dash class which can then be run on localhost.
    """
    app = Dash(__name__)
    tbl1 = df_to_dt(df1, "tbl1")
    tbl2 = df_to_dt(df2, "tbl2")
    return layout(app, tbl1, tbl2)


def layout(app: Dash, tbl1: DT, tbl2: DT) -> Dash():
    """Creates the layout of the dash application."""
    app.layout = html.Div([
        html.H2("Damage Done"),
        tbl1,
        html.H2("Healing Done"),
        tbl2,
    ], style={"backgroundColor": "#161a1d", "padding": 40})
    return app


def df_to_dt(df: pd.DataFrame, id: str) -> DT:
    """Converts dataframe into DataTable, using previously defined styles."""
    r_column = "rDPS" if "rDPS" in df.columns else "rHPS"
    return DT(df.to_dict("records"),
              [{"name": i, "id": i, "selectable": True} for i in df.columns],
              id=id,
              sort_action="native",
              style_as_list_view=True,
              style_cell=styles("cell"),
              style_header=styles("header"),
              style_data=styles("table_data"),
              style_data_conditional=(
                  data_bars(df, "Amount Total") +
                  data_bars(df, r_column) +
                  parse_colors(df)),
              style_cell_conditional=column_width(df)
              )


# The following 4 methods are all only relevant for the dashboards style.

def styles(type: str) -> dict:
    """Returns dictionary of styles as specified by "type"."""
    if type == "header":
        return {
            "backgroundColor": "#0e1012",
            "color": "white"
        }
    elif type == "table_data":
        return {
                "backgroundColor": "#161a1d",
                "color": "white"
        }
    elif type == "cell":
        return {
            "font_size": "18px",
            "border": "1px solid #3f3f3f"
        }


def data_bars(df: pd.DataFrame, column: str) -> dict:
    """Conditional formatting for data bars in cells.

    Creates a conditional formatting dictionary that shows data bars inside of
    (data-)table cells. Bar lengths are relative to the highest value.

    .. note::
        This method was taken from the `official dash documentation
        <https://dash.plotly.com/datatable/conditional-formatting>`_ and
        slightly adjusted.

    Args:
      df:
        The pandas dataframe in question.
      column:
        The name of the column where bars are shown.

    Returns:
      A dictionary of conditional formatting that can be used to style a
      dash DataTable.
    """
    bar_color = "#f4d44d" if "DPS" in df.columns else "#91dfd2"
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
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


def column_width(df: pd.DataFrame) -> dict:
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
    if "HPS" in df.columns:
        styles.append({"if": {"column_id": "Amount Total"}, "width": "45%"})
    else:
        styles.append({"if": {"column_id": "Amount Total"}, "width": "50%"})
    return styles


def parse_colors(df: pd.DataFrame) -> dict:
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
