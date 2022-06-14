"""Main control flow."""

from input import user_input as ui
from data import data_scraping as ds
# from data import data_combination as dc
# from data import data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    links = ui.user_input()
    data = ds.scrape()
    print(data)


main()
