"""Climate GHCN data"""

import re

import numpy as np
import pandas as pd


def ghcn_read_stations_file():
    """Read GHCN stations file"""
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
    spec = {
        "id": [(0, 11), str],
        "latitude": [(12, 20), float],
        "longitude": [(21, 30), float],
        "elevation": [(31, 37), float],
        "state": [(38, 40), str],
        "name": [(41, 71), str],
        "gsn_flag": [(72, 75), str],
        "hcn_flag": [(76, 79), str],
        "wmo_id": [(80, 85), str],
    }
    names = spec.keys()
    values = spec.values()
    colspecs = [x[0] for x in values]
    dtypes = [x[1] for x in values]
    dtypes = dict(zip(names, dtypes))
    try:
        df = pd.read_fwf(path, colspecs=colspecs, names=names, dtype=dtypes)
    except Exception as e:
        print("Exception: ", e, " at ", path)
    return df


def ghcn_read_dly_file(id1=None, path=None):
    """Read GHCN dly file

    Use "id1" for the ID of the file.

    Use "path" for the full path name of the file.
    """
    if id1 is not None:
        path = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/" + str(id1) + ".dly"
    elif id1 is None and path is None:
        raise ValueError("id1 or path must be used")
    spec1 = {
        "id": [(0, 11), str],
        "year": [(11, 15), float],
        "month": [(15, 17), float],
        "element": [(17, 21), str],
    }
    spec2 = {"value" + str(i): [(13 + i * 8, 18 + i * 8), float] for i in range(1, 32)}
    spec = {**spec1, **spec2}
    names = spec.keys()
    values = spec.values()
    colspecs = [x[0] for x in values]
    dtypes = [x[1] for x in values]
    dtypes = dict(zip(names, dtypes))
    try:
        df = pd.read_fwf(
            path,
            colspecs=colspecs,
            names=names,
            dtype=dtypes,
            na_values=["", "-9999"],
            keep_default_na=False,
        )
    except Exception as e:
        print("Exception: ", e, " at ", path)
    return df


def ghcn_clean_dly_data(df):
    """Clean dly data"""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a dataframe")
    col = ["id", "year", "month", "element"] + ["value" + str(i) for i in range(1, 32)]
    ind = df["element"].isin(["PRCP", "SNOW", "SNWD", "TMAX", "TMIN"])
    df = df.loc[ind, col]
    df = pd.melt(df, id_vars=["id", "year", "month", "element"])
    day = [re.sub("value", "", x) for x in df["variable"].tolist()]
    df["date"] = pd.to_datetime(
        {"year": df["year"], "month": df["month"], "day": day}, errors="coerce"
    )
    df = df[["id", "date", "element", "value"]]
    df = df[~df["date"].isna()]
    df["value"] = ghcn_clean_values(df["value"], df["element"])
    df = pd.pivot_table(
        df, index=["id", "date"], columns="element", values="value"
    ).reset_index()
    df.columns = [x.lower() for x in df.columns]
    for col in ["prcp"]:
        df[col] = df[col].round(2)
    for col in ["snow", "snwd", "tmax", "tmin"]:
        df[col] = df[col].round(1)
    return df


def ghcn_clean_values(x, element):
    """Clean five core element values"""
    x = x.to_numpy()
    x[element == "PRCP"] = x[element == "PRCP"] / 254
    x[element == "SNOW"] = x[element == "SNOW"] / 25.4
    x[element == "SNWD"] = x[element == "SNWD"] / 25.4
    x[element == "TMAX"] = x[element == "TMAX"] * 0.18 + 32
    x[element == "TMIN"] = x[element == "TMIN"] * 0.18 + 32
    return x

