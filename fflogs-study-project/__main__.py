"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
from data import data_combination as dc
from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    links = ui.user_input(2)
    spider = ds.Scraping(links, headless=True)

    spider.parse_logs()

    df_lists = dc.csv_to_dfs()

    dd = dc.join_dd_dfs(df_lists[0])
    hd = dc.join_hd_dfs(df_lists[1])

    dv.dash(dd, hd).run_server(debug=False, port=8053)


main()
