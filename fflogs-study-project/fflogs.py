"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
from data import data_combination as dc
from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    # input = ui.user_input()

    # spider = ds.Scraping(input.logs, type=input.type, headless=input.headless)
    # spider.parse_logs()

    df_lists = dc.csv_to_dfs()

    dd = dc.join_dd_dfs(df_lists[0])
    hd = dc.join_hd_dfs(df_lists[1])

    # dv.dash(dd, hd).run_server(debug=input.debug, use_reloader=False, port=8055)
    dv.dash(dd, hd).run_server(debug=True, port=8056)
