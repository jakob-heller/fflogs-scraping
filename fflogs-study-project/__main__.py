"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
from data import data_combination as dc
# from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    links = ui.user_input()
    spider = ds.Scraping(links, "wipes", headless=True)

    spider.parse_logs()

    df_lists = dc.csv_to_dfs()

    print(dc.join_dd_dfs(df_lists[0]))
    print(dc.join_hd_dfs(df_lists[1]))


main()
