"""Interactively visualize data using a basic Dash data app."""

from dash import Dash, Input, Output, html, dcc
from dash import dash_table as dt
import plotly.express as px
import pandas as pd


def dash(df1: pd.DataFrame, df2: pd.DataFrame) -> Dash():
    """Do this."""
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    notice = """
        Select a column to plot metric against player names.
        When sorting columns, you have to change the column
        selection in any kind of way for the names to adjust in the
        graph. This is a bug that I have not been able to fix.
    """

    table1 = dt.DataTable(df1.to_dict('records'),
                          [{"name": i, "id": i, "selectable": True} for i in df1.columns],
                          id='tbl1',
                          sort_action="native",
                          column_selectable="single")
    table2 = dt.DataTable(df2.to_dict('records'),
                          [{"name": i, "id": i, "selectable": True} for i in df2.columns],
                          id='tbl2',
                          sort_action="native",
                          column_selectable="single")

    app.layout = html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Damage Done', value='tab-1', children=[
                table1,
                dcc.Graph(id="dyn-graph-1", animate=False)
            ]),
            dcc.Tab(label='Healing Done', value='tab-2', children=[
                table2,
                dcc.Graph(id="dyn-graph-2", animate=False)
            ]),
        ]),
        html.Div(id='tabs-content')
    ])

    @app.callback(Output('tabs-content', 'children'),
                  Input('tabs', 'value'))
    def render_content(tab):
        if tab == 'tab-1':
            return html.Div([
                html.H3(notice)
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.H3(notice)
            ])

    @app.callback(Output("dyn-graph-1", "figure"),
                  Input('tbl1', "derived_viewport_data"),
                  Input("tbl1", "derived_viewport_selected_columns"))
    def update_figure1(data, selected_column):
        dff1 = df1 if selected_column is None else pd.DataFrame(data)
        fig = px.bar(dff1, x=selected_column, y="Name", orientation='h')
        fig['layout']['yaxis']['autorange'] = "reversed"
        fig.update_layout(transition_duration=500)
        return fig

    @app.callback(Output("dyn-graph-2", "figure"),
                  Input('tbl2', "derived_viewport_data"),
                  Input("tbl2", "derived_viewport_selected_columns"))
    def update_figure2(data, selected_column):
        dff2 = df2 if selected_column is None else pd.DataFrame(data)
        fig = px.bar(dff2, x=selected_column, y="Name", orientation='h')
        fig['layout']['yaxis']['autorange'] = "reversed"
        fig.update_layout(transition_duration=500)
        return fig

    return app
