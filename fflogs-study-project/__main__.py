"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
# from data import data_combination as dc
# from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    links = ui.user_input()
    spider = ds.Scraping(links, "wipes", headless=True)

    spider.parse_logs()

    print(spider.comp)


main()
