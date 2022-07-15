"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
from data import data_combination as dc
from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    inpt = ui.user_input()

    spider = ds.Scraping(inpt.logs, type=inpt.type, headless=inpt.headless)
    spider.parse_logs()

    df_lists = dc.csv_to_dfs()

    dd = dc.join_dd_dfs(df_lists[0])
    hd = dc.join_hd_dfs(df_lists[1])

    dv.dash(dd, hd).run_server(debug=inpt.debug, use_reloader=False, port=8058)
    # dv.dash(dd, hd).run_server(debug=True, port=8056)
