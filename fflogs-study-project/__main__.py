"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
# from data import data_combination as dc
# from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    links = ui.user_input()
    spider = ds.Scraping(links, "kills", headless=False)

    spider.parse_logs()

    print(spider.comp)
    print(f"List of healing done dfs: {spider.hd_dfs}.")
    print(f"List of damage dealt dfs: {spider.dd_dfs}.")


main()
