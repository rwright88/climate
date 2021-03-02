"""Climate normals daily data"""

import re

import numpy as np
import pandas as pd


def norm_get_dly():
    """Get all daily climate normals data"""
    prcp = norm_get_dly_prcp()
    snow = norm_get_dly_snow()
    tavg = norm_get_dly_tavg()
    tmax = norm_get_dly_tmax()
    tmin = norm_get_dly_tmin()
    by = ["id", "month", "day"]
    df = pd.merge(prcp, snow, how="outer", on=by)
    df = pd.merge(df, tavg, how="outer", on=by)
    df = pd.merge(df, tmax, how="outer", on=by)
    df = pd.merge(df, tmin, how="outer", on=by)
    df = df.sort_values(by)
    return df


def norm_get_dly_prcp():
    path = "https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/precipitation/dly-prcp-pctall-ge010hi.txt"
    df = norm_read_dly_file(path)
    df = pd.melt(df, id_vars=["id", "month"])
    df.columns = ["id", "month", "day", "prcp"]
    df["day"] = fix_day(df["day"])
    df["prcp"] = df["prcp"] / 10
    return df


def norm_get_dly_snow():
    path = "https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/precipitation/dly-snow-pctall-ge010ti.txt"
    df = norm_read_dly_file(path)
    df = pd.melt(df, id_vars=["id", "month"])
    df.columns = ["id", "month", "day", "snow"]
    df["day"] = fix_day(df["day"])
    df["snow"] = df["snow"] / 10
    return df


def norm_get_dly_tavg():
    path = "https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tavg-normal.txt"
    df = norm_read_dly_file(path)
    df = pd.melt(df, id_vars=["id", "month"])
    df.columns = ["id", "month", "day", "tavg"]
    df["day"] = fix_day(df["day"])
    df["tavg"] = df["tavg"] / 10
    return df


def norm_get_dly_tmax():
    path = "https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmax-normal.txt"
    df = norm_read_dly_file(path)
    df = pd.melt(df, id_vars=["id", "month"])
    df.columns = ["id", "month", "day", "tmax"]
    df["day"] = fix_day(df["day"])
    df["tmax"] = df["tmax"] / 10
    return df


def norm_get_dly_tmin():
    path = "https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/dly-tmin-normal.txt"
    df = norm_read_dly_file(path)
    df = pd.melt(df, id_vars=["id", "month"])
    df.columns = ["id", "month", "day", "tmin"]
    df["day"] = fix_day(df["day"])
    df["tmin"] = df["tmin"] / 10
    return df


def fix_day(x):
    return pd.to_numeric([re.sub("day", "", e) for e in x])


def norm_read_dly_file(path):
    """Read a normals daily file"""
    spec1 = {"id": [(0, 11), str], "month": [(12, 14), float]}
    spec2 = {"day" + str(i): [(11 + i * 7, 16 + i * 7), float] for i in range(1, 32)}
    spec = {**spec1, **spec2}
    names = spec.keys()
    values = spec.values()
    colspecs = [x[0] for x in values]
    dtypes = [x[1] for x in values]
    dtypes = dict(zip(names, dtypes))
    na = ["-5555", "-6666", "-7777", "-8888", "-9999"]
    try:
        df = pd.read_fwf(
            path,
            colspecs=colspecs,
            names=names,
            dtype=dtypes,
            na_values=na,
            keep_default_na=False,
        )
    except Exception as e:
        print("Exception: ", e, " at ", path)
    return df

