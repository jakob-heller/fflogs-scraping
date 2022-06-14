"""Calls all functions."""

from input import user_input as ui
# from data import data_scraping
# import data_combination
# import data_visualization


def main():
    links = ui.user_input()
    print(links)


main()
