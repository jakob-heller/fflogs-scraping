"""
CSV files are read to pandas dataframes, cleaned, concatenated and summarized.
"""

import os
import glob
import pandas as pd


def csv_to_dfs() -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """Reads csv files.

    Reads csv files in csv directory as pandas dataframes and adds them either
    to a "damage", or to a "healing" list, depending on their structure.

    Returns:
      2-tuple of lists of dataframes, one for damage and one for healing.
    """
    dd_dfs = []
    hd_dfs = []

    for filename in get_csv_paths():
        df = pd.read_csv(filename, na_values=["-"]).fillna(0)
        # "Limit Break" row contains useless information so we drop it.
        df = (df.set_index("Name").drop(labels="Limit Break", errors="ignore")
              .reset_index())
        if "DPS" in df.columns:
            dd_dfs.append(df)
        else:
            hd_dfs.append(df)
    return (dd_dfs, hd_dfs)


def get_csv_paths() -> list[str]:
    """Returns a list of relative paths to csv files in the csv directory."""
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(dirname, "csv")
    return glob.glob(os.path.join(csv_path, "*.csv"))


def join_dd_dfs(dd_df_list: list[pd.DataFrame]) -> pd.DataFrame:
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
    dd_df = convert_df(dd_df, "DPS")
    dd_df = aggregate_dd(dd_df)
    dd_df = fix_columns_dd(dd_df)

    dd_df["Parse %"] = dd_df["Parse %"].round()
    dd_df = dd_df.round(decimals=2)
    return dd_df


def join_hd_dfs(hd_df_list: list[pd.DataFrame]) -> pd.DataFrame:
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
    hd_df = convert_df(hd_df, "HPS")
    hd_df = aggregate_hd(hd_df)
    hd_df = fix_columns_hd(hd_df)

    hd_df["Parse %"] = hd_df["Parse %"].round()
    hd_df = hd_df.round(decimals=2)
    return hd_df


def convert_df(df: pd.DataFrame, type: str) -> pd.DataFrame:
    """Converts values to numeric values.

    To be able to summarize the data, all values need to be converted to
    numeric first. The "Amount" column has 3 values separated by special
    characters, 2 of which get split into their own columns.

    Args:
      dd_df:
        Pandas dataframe that has just been concatenated.
      type:
        Either "HPS" or "DPS" - both have slightly different columns and thus
        need to be handled differently.

    Returns:
      Dataframe where all relevant values have been converted to numeric
      (except "Name" column).
    """
    df["Parse %"] = pd.to_numeric(df["Parse %"])
    df[type] = pd.to_numeric(df[type].str.replace(",", ""))
    df[f"r{type}"] = pd.to_numeric(df[f"r{type}"].str.replace(",", ""))
    df["Active"] = pd.to_numeric(df["Active"].str.split("%").str[0])
    amt_series = df["Amount"].str.split("$")
    df["amt"] = pd.to_numeric(amt_series.str[0])
    df["amt_pct"] = pd.to_numeric(amt_series.str[1].str.split("%").str[0])

    if type == "HPS":
        df["Overheal"] = pd.to_numeric(df["Overheal"].str.split("%").str[0])
    return df


def aggregate_dd(df: pd.DataFrame) -> pd.DataFrame:
    """Returns dataframe aggregated by "Name" column."""
    return df.set_index("Name").groupby("Name").agg(
        parse_pct=("Parse %", "mean"),
        amount_pct=("amt_pct", "mean"),
        amount=("amt", "sum"),
        active_pct=("Active", "mean"),
        DPS=("DPS", "mean"),
        rDPS=("rDPS", "mean")
    ).reset_index()


def aggregate_hd(df: pd.DataFrame) -> pd.DataFrame:
    """Returns dataframe aggregated by "Name" column."""
    return df.set_index("Name").groupby("Name").agg(
        parse_pct=("Parse %", "mean"),
        amount_pct=("amt_pct", "mean"),
        amount=("amt", "sum"),
        overheal=("Overheal", "mean"),
        active_pct=("Active", "mean"),
        HPS=("HPS", "mean"),
        rHPS=("rHPS", "mean")
    ).reset_index()


def fix_columns_dd(df: pd.DataFrame) -> pd.DataFrame:
    """Fixes and sets better looking column names for later visualization."""
    columns_titles = ["parse_pct", "Name", "amount_pct",
                      "amount", "active_pct", "DPS", "rDPS"]
    new_titles = {"parse_pct": "Parse %", "Name": "Player Name",
                  "amount_pct": "Amount %", "amount": "Amount Total",
                  "active_pct": "Active %", "HPS": "HPS", "rDPS": "rDPS"}
    return df.reindex(columns=columns_titles).rename(columns=new_titles)


def fix_columns_hd(df: pd.DataFrame) -> pd.DataFrame:
    """Fixes and sets better looking column names for later visualization."""
    columns_titles = ["parse_pct", "Name", "amount_pct", "amount",
                      "overheal", "active_pct", "HPS", "rHPS"]
    new_titles = {"parse_pct": "Parse %", "Name": "Player Name",
                  "amount_pct": "Amount %", "amount": "Amount Total",
                  "overheal": "Overheal", "active_pct": "Active %",
                  "HPS": "HPS", "rHPS": "rHPS"}
    return df.reindex(columns=columns_titles).rename(columns=new_titles)
