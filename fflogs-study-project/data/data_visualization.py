"""Interactively visualize data using a basic Dash data app."""

from dash import Dash, Input, Output, html, dcc
from dash.dash_table import DataTable as DT
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc


def data_bars(df: pd.DataFrame, column: str) -> dict:
    """Conditional formatting for data bars in cells.

    Taken from dash documentation:
    https://dash.plotly.com/datatable/conditional-formatting
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
            'if': {
                'filter_query': (
                    f'{{{column}}} >= {min_bound}' +
                    (f' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ),
                'column_id': column
            },
            'background': (
                f"""
                    linear-gradient(90deg,
                    {bar_color} 0%,
                    {bar_color} {max_bound_percentage}%,
                    #242a44 {max_bound_percentage}%,
                    #242a44 100%
                """
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })
        styles.append({
            "if": {"state": "selected"},
            "backgroundColor": "#f45060",
            "border": "inherit !important",
        })
    return styles


def parse_colors(df: pd.DataFrame, column: str) -> dict:
    """Assign the correct colors to respective parse values."""
    styles = [
        {
            'if': {
                'filter_query': '{Parse %} > 0 && {Parse %} < 25',
                'column_id': 'Parse %'
            },
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} > 24 && {Parse %} < 50',
                'column_id': 'Parse %'
            },
            'color': '#1bb607',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} > 49 && {Parse %} < 75',
                'column_id': 'Parse %'
            },
            'color': '#035fb9',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} > 74 && {Parse %} < 95',
                'column_id': 'Parse %'
            },
            'color': '#822dbc',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} = 99',
                'column_id': 'Parse %'
            },
            'color': '#db7ea7',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} = 100',
                'column_id': 'Parse %'
            },
            'color': '#b29f65',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Parse %} > 0 && {Parse %} < 26',
                'column_id': 'Parse %'
            },
            'color': '#1cd404',
            'fontWeight': 'bold'
        }
    ]
    return styles


def column_width(df: pd.DataFrame) -> dict:
    """Return dictionary for column widths."""
    styles = [
        {'if': {'column_id': 'Parse %'},
         'width': '5%'},
        {'if': {'column_id': 'Player Name'},
         'width': '10%'},
        {'if': {'column_id': 'Amount %'},
         'width': '5%'},
        {'if': {'column_id': 'Active %'},
         'width': '5%'},
        {'if': {'column_id': 'DPS'},
         'width': '5%'},
        {'if': {'column_id': 'rDPS'},
         'width': '15%'},
        {'if': {'column_id': 'HPS'},
         'width': '5%'},
        {'if': {'column_id': 'rHPS'},
         'width': '15%'},
        {'if': {'column_id': 'Overheal'},
         'width': '5%'}
    ]
    # The healing table as one column more, I make "amount" smaller there.
    if 'HPS' in df.columns:
        styles.append(
            {'if': {'column_id': 'Amount Total'},
             'width': '45%'},
        )
    else:
        styles.append(
            {'if': {'column_id': 'Amount Total'},
             'width': '50%'},
        )
    return styles


def dash(df1: pd.DataFrame, df2: pd.DataFrame) -> Dash():
    """Create an interactive Dashboard with 2 tabs.

    Args:
      df1: pd.DataFrame, dataframe of summarized damage done.
      df2: pd.DataFrame, dataframe of summarized healing done.

    Returns:
      Object of Dash class.
    """
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    # app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    # app = Dash(__name__)

    style_table_header = {
        'backgroundColor': '#0e1012',
        'color': 'white'
    }
    style_table_data = {
        'backgroundColor': '#161a1d',
        'color': 'white'
    }
    style_cell = {
        'font_size': '18px',
        'border': '1px solid #3f3f3f'
    }
    # Convert dataframes to sortable dash datatables.
    tbl1 = DT(df1.to_dict('records'),
              [{"name": i, "id": i, "selectable": True} for i in df1.columns],
              id='tbl1',
              sort_action="native",
              style_as_list_view=True,
              style_cell=style_cell,
              style_header=style_table_header,
              style_data=style_table_data,
              style_data_conditional=(
                  data_bars(df1, 'Amount Total') +
                  data_bars(df1, 'rDPS') +
                  parse_colors(df1, 'Parse %')),
              style_cell_conditional=column_width(df1)
              )
    tbl2 = DT(df2.to_dict('records'),
              [{"name": i, "id": i, "selectable": True} for i in df2.columns],
              id='tbl2',
              sort_action="native",
              style_as_list_view=True,
              style_cell=style_cell,
              style_header=style_table_header,
              style_data=style_table_data,
              style_data_conditional=(
                  data_bars(df2, 'Amount Total') +
                  data_bars(df2, 'rHPS') +
                  parse_colors(df2, 'Parse %')),
              style_cell_conditional=column_width(df2)
              )
    app.layout = html.Div([
        html.H2("Damage Done"),
        tbl1,
        html.H2("Healing Done"),
        tbl2,
    ], style={'backgroundColor': '#161a1d', 'padding': 40})

    return app
