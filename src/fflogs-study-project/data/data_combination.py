"""Includes csv reading, loading and meaningful combination."""

import os
import glob
import pandas as pd


def csv_to_dfs() -> tuple:
    """Reads csv files.

    Reads csv files in csv directory as pandas dataframes and adds them either
    to a "damage", or to a "healing" list, depending on their structure.

    Returns:
      2-tuple of lists of dataframes, one for damage and one for healing.
    """
    dd_dfs = []
    hd_dfs = []

    # We get a list of relative paths to csv files in the csv directory to
    # iterate over.
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(dirname, "csv")
    all_csvs = glob.glob(os.path.join(csv_path, "*.csv"))

    for filename in all_csvs:
        df = pd.read_csv(filename, na_values=["-"]).fillna(0)
        # "Limit Break" row contains useless information so we drop it.
        df = (df.set_index("Name").drop(labels="Limit Break", errors="ignore")
              .reset_index())
        if "DPS" in df.columns:
            dd_dfs.append(df)
        else:
            hd_dfs.append(df)
    return (dd_dfs, hd_dfs)


def join_dd_dfs(dd_df_list: list) -> pd.DataFrame:
    """Joins multiple "damage done" dataframes to single dataframe.

    Concatenates all dataframes provided into one dataframe, converts all
    values (except for column "Name") into numeric values, reorders and renames
    columns.

    Args:
      dd_df_list:
        A list of pandas dataframes with identical structure and data
        referring to the "damage done" metric.

    Returns:
      The returned pd.DataFrame is the summary of the given dataframes, ready
      to be visualized.
    """
    dd_df = pd.concat(dd_df_list)

    # To be able to summarize the data, all values need to be converted to
    # numeric first. The "Amount" column has 3 values separated by special
    # characters, 2 of which get split into their own columns.
    dd_df["Parse %"] = pd.to_numeric(dd_df["Parse %"])
    dd_df["DPS"] = pd.to_numeric(dd_df["DPS"].str.replace(",", ""))
    dd_df["rDPS"] = pd.to_numeric(dd_df["rDPS"].str.replace(",", ""))
    dd_df["Active"] = pd.to_numeric(dd_df["Active"].str.split("%").str[0])
    amt_series = dd_df["Amount"].str.split("$")
    dd_df["amt"] = pd.to_numeric(amt_series.str[0])
    dd_df["amt_pct"] = pd.to_numeric(amt_series.str[1].str.split("%").str[0])

    dd_df = dd_df.set_index("Name").groupby("Name").agg(
        parse_pct=("Parse %", "mean"),
        amount_pct=("amt_pct", "mean"),
        amount=("amt", "sum"),
        active_pct=("Active", "mean"),
        DPS=("DPS", "mean"),
        rDPS=("rDPS", "mean")
    ).reset_index()

    # Since we used "Name" as an index for aggregation, we fix the column names
    # and set better looking column names for later visualization.
    columns_titles = ["parse_pct", "Name", "amount_pct",
                      "amount", "active_pct", "DPS", "rDPS"]
    dd_df = dd_df.reindex(columns=columns_titles)
    new_titles = {"parse_pct": "Parse %", "Name": "Player Name",
                  "amount_pct": "Amount %", "amount": "Amount Total",
                  "active_pct": "Active %", "HPS": "HPS", "rDPS": "rDPS"}
    dd_df = dd_df.rename(columns=new_titles)

    dd_df["Parse %"] = dd_df["Parse %"].round()
    dd_df = dd_df.round(decimals=2)
    return dd_df


def join_hd_dfs(hd_df_list: list) -> pd.DataFrame:
    """Joins multiple "healing done" dataframes to single dataframe.

    Mostly identical to join_dd_dfs(), split up into two functions because the
    structure of the given dataframes are slightly different in both cases.

    Args:
      dd_df_list:
        A list of pandas dataframes with identical structure and data
        referring to the "healing done" metric.

    Returns:
      The returned pd.DataFrame is the summary of the given dataframes, ready
      to be visualized.
    """
    hd_df = pd.concat(hd_df_list)

    # To be able to summarize the data, all values need to be converted to
    # numeric first. The "Amount" column has 3 values separated by special
    # characters, 2 of which get split into their own columns.
    hd_df["Parse %"] = pd.to_numeric(hd_df["Parse %"])
    hd_df["HPS"] = pd.to_numeric(hd_df["HPS"].str.replace(",", ""))
    hd_df["rHPS"] = pd.to_numeric(hd_df["rHPS"].str.replace(",", ""))
    hd_df["Active"] = pd.to_numeric(hd_df["Active"].str.split("%").str[0])
    hd_df["Overheal"] = pd.to_numeric(hd_df["Overheal"].str.split("%").str[0])
    amt_series = hd_df["Amount"].str.split("$")
    hd_df["amt"] = pd.to_numeric(amt_series.str[0])
    hd_df["amt_pct"] = pd.to_numeric(amt_series.str[1].str.split("%").str[0])

    hd_df = hd_df.set_index("Name").groupby("Name").agg(
        parse_pct=("Parse %", "mean"),
        amount_pct=("amt_pct", "mean"),
        amount=("amt", "sum"),
        overheal=("Overheal", "mean"),
        active_pct=("Active", "mean"),
        HPS=("HPS", "mean"),
        rHPS=("rHPS", "mean")
    ).reset_index()

    # Since we used "Name" as an index for aggregation, we fix the column names
    # and set better looking column names for later visualization.
    columns_titles = ["parse_pct", "Name", "amount_pct", "amount",
                      "overheal", "active_pct", "HPS", "rHPS"]
    hd_df = hd_df.reindex(columns=columns_titles)
    new_titles = {"parse_pct": "Parse %", "Name": "Player Name",
                  "amount_pct": "Amount %", "amount": "Amount Total",
                  "overheal": "Overheal", "active_pct": "Active %",
                  "HPS": "HPS", "rHPS": "rHPS"}
    hd_df = hd_df.rename(columns=new_titles)

    hd_df["Parse %"] = hd_df["Parse %"].round()
    hd_df = hd_df.round(decimals=2)
    return hd_df
