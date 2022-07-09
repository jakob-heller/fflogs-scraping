"""Includes csv reading, loading and meaningful combination."""

import os
import glob

import pandas as pd


def csv_to_dfs() -> tuple:
    """Read csv files as dfs, add them to list according to DPS/HPS."""
    dd_dfs = []
    hd_dfs = []

    # Get relative path to csv folder
    dirname = os.path.dirname(__file__)
    csv_path = os.path.join(dirname, "csv")

    # Get list of paths of every downloaded csv file
    all_csvs = glob.glob(os.path.join(csv_path, "*.csv"))

    for filename in all_csvs:
        df = pd.read_csv(filename, na_values=["-"])
        # "Limit Break" contains useless information (if present at all).
        try:
            df = df.set_index("Name").drop(labels="Limit Break").reset_index()
        except KeyError:
            pass
        # Append to dd_dfs if it contains column "DPS", to hd_dfs if not.
        try:
            df.loc[:, "DPS"]
            dd_dfs.append(df)
        except KeyError:
            hd_dfs.append(df)

    return (dd_dfs, hd_dfs)


def join_dd_dfs(dd_df_list: list) -> pd.DataFrame:
    """Concatenate dataframes, convert to numeric values and aggregate."""
    dd_df = pd.concat(dd_df_list)

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

    return dd_df


def join_hd_dfs(hd_df_list: list) -> pd.DataFrame:
    """Concatenate dataframes, convert to numeric values and aggregate."""
    hd_df = pd.concat(hd_df_list)

    hd_df["Parse %"] = pd.to_numeric(hd_df["Parse %"])
    hd_df["HPS"] = pd.to_numeric(hd_df["HPS"].str.replace(",", ""))
    hd_df["rHPS"] = pd.to_numeric(hd_df["rHPS"].str.replace(",", ""))

    hd_df["Active"] = pd.to_numeric(hd_df["Active"].str.split("%").str[0])
    hd_df["Overheal"] = pd.to_numeric(hd_df["Overheal"].str.split("%").str[0])

    amt_series = hd_df["Amount"].str.split("$")
    hd_df["amt"] = pd.to_numeric(amt_series.str[0])
    hd_df["amt_pct"] = pd.to_numeric(amt_series.str[1].str.split("%").str[0])

    hd_df = hd_df.set_index("Name").groupby("Name").agg(
        Parse_pct=("Parse %", "mean"),
        Amount_pct=("amt_pct", "mean"),
        Amount=("amt", "sum"),
        Overheal=("Overheal", "mean"),
        Active_pct=("Active", "mean"),
        DPS=("HPS", "mean"),
        rDPS=("rHPS", "mean")
    ).reset_index()

    return hd_df
