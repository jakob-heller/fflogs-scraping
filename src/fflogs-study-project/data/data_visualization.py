"""Interactively visualize data using a basic Dash data app."""

import pandas as pd
from dash import Dash, html
from dash.dash_table import DataTable as DT


def data_bars(df: pd.DataFrame, column: str) -> dict:
    """Conditional formatting for data bars in cells.

    Creates a conditional formatting dictionary that shows data bars inside of
    (data-)table cells. Bar lengths are relative to the highest value.

    Taken from dash documentation and slightly adjusted:
    https://dash.plotly.com/datatable/conditional-formatting

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
                "filter_query": "{Parse %} > 0 && {Parse %} < 25",
                "column_id": "Parse %"
            },
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
        {
            "if": {
                "filter_query": "{Parse %} > 0 && {Parse %} < 26",
                "column_id": "Parse %"
            },
            "color": "#1cd404",
            "fontWeight": "bold"
        }
    ]
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
      Object of Dash class which can then be run on a loc.
    """
    app = Dash(__name__)

    # Some more styles to use later
    style_table_header = {
        "backgroundColor": "#0e1012",
        "color": "white"
    }
    style_table_data = {
        "backgroundColor": "#161a1d",
        "color": "white"
    }
    style_cell = {
        "font_size": "18px",
        "border": "1px solid #3f3f3f"
    }
    # We convert our dataframes to sortable dash datatables using the styles
    # we defined before.
    tbl1 = DT(df1.to_dict("records"),
              [{"name": i, "id": i, "selectable": True} for i in df1.columns],
              id="tbl1",
              sort_action="native",
              style_as_list_view=True,
              style_cell=style_cell,
              style_header=style_table_header,
              style_data=style_table_data,
              style_data_conditional=(
                  data_bars(df1, "Amount Total") +
                  data_bars(df1, "rDPS") +
                  parse_colors(df1)),
              style_cell_conditional=column_width(df1)
              )
    tbl2 = DT(df2.to_dict("records"),
              [{"name": i, "id": i, "selectable": True} for i in df2.columns],
              id="tbl2",
              sort_action="native",
              style_as_list_view=True,
              style_cell=style_cell,
              style_header=style_table_header,
              style_data=style_table_data,
              style_data_conditional=(
                  data_bars(df2, "Amount Total") +
                  data_bars(df2, "rHPS") +
                  parse_colors(df2)),
              style_cell_conditional=column_width(df2)
              )
    app.layout = html.Div([
        html.H2("Damage Done"),
        tbl1,
        html.H2("Healing Done"),
        tbl2,
    ], style={"backgroundColor": "#161a1d", "padding": 40})

    return app
