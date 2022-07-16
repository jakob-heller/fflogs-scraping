"""Main control flow."""

import input.user_input as ui
import data.data_scraping as ds
import data.data_combination as dc
import data.data_visualization as dv


def main():
    """Get links from user, scrape data, combine and visualize."""
    inpt = ui.user_input()

    print("\nStarting Webdriver...", flush=True, end=" ")
    spider = ds.Scraping(inpt.logs, type=inpt.type, headless=inpt.headless)
    print("...Webdriver started.")
    spider.parse_logs()

    print("Combining data...", flush=True, end=" ")
    df_lists = dc.csv_to_dfs()
    dd = dc.join_dd_dfs(df_lists[0])
    hd = dc.join_hd_dfs(df_lists[1])
    print("...combination finished.")

    print("\nLaunching Dash application on localhost:\n")
    dv.dash(dd, hd).run_server(debug=inpt.debug, use_reloader=False, port=inpt.port)


def debug():
    """main() without the scraping part to work on the dashboard."""
    df_lists = dc.csv_to_dfs()
    dd = dc.join_dd_dfs(df_lists[0])
    hd = dc.join_hd_dfs(df_lists[1])
    dv.dash(dd, hd).run_server(debug=True)
