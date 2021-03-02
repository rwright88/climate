"""Climate normals monthly data"""

import re

import numpy as np
import pandas as pd


def norm_get_mly():
    """Get all monthly climate normals data"""
    prcp = norm_get_mly_prcp()
    snow = norm_get_mly_snow()
    tavg = norm_get_mly_tavg()
    tmax = norm_get_mly_tmax()
    tmin = norm_get_mly_tmin()
    df = pd.merge(prcp, snow, how="outer", on=["id", "month"])
    df = pd.merge(df, tavg, how="outer", on=["id", "month"])
    df = pd.merge(df, tmax, how="outer", on=["id", "month"])
    df = pd.merge(df, tmin, how="outer", on=["id", "month"])
    return df


def norm_get_mly_prcp():
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/normals/1981-2010/products/precipitation/mly-prcp-normal.txt"
    df = norm_read_mly_file(path)
    df = pd.melt(df, id_vars=["id"])
    df.columns = ["id", "month", "prcp"]
    df["month"] = fix_month(df["month"])
    df["prcp"] = df["prcp"] / 100
    return df


def norm_get_mly_snow():
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/normals/1981-2010/products/precipitation/mly-snow-normal.txt"
    df = norm_read_mly_file(path)
    df = pd.melt(df, id_vars=["id"])
    df.columns = ["id", "month", "snow"]
    df["month"] = fix_month(df["month"])
    df["snow"] = df["snow"] / 10
    return df


def norm_get_mly_tavg():
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/mly-tavg-normal.txt"
    df = norm_read_mly_file(path)
    df = pd.melt(df, id_vars=["id"])
    df.columns = ["id", "month", "tavg"]
    df["month"] = fix_month(df["month"])
    df["tavg"] = df["tavg"] / 10
    return df


def norm_get_mly_tmax():
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/mly-tmax-normal.txt"
    df = norm_read_mly_file(path)
    df = pd.melt(df, id_vars=["id"])
    df.columns = ["id", "month", "tmax"]
    df["month"] = fix_month(df["month"])
    df["tmax"] = df["tmax"] / 10
    return df


def norm_get_mly_tmin():
    path = "ftp://ftp.ncdc.noaa.gov/pub/data/normals/1981-2010/products/temperature/mly-tmin-normal.txt"
    df = norm_read_mly_file(path)
    df = pd.melt(df, id_vars=["id"])
    df.columns = ["id", "month", "tmin"]
    df["month"] = fix_month(df["month"])
    df["tmin"] = df["tmin"] / 10
    return df


def fix_month(x):
    return pd.to_numeric([re.sub("month", "", e) for e in x])


def norm_read_mly_file(path):
    """Read a normals monthly file"""
    spec1 = {"id": [(0, 11), str]}
    spec2 = {"month" + str(i): [(11 + i * 7, 16 + i * 7), float] for i in range(1, 13)}
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

