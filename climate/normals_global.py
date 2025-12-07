"""Climate normals monthly data, global"""

import numpy as np
import pandas as pd


def norm_get_mly_glb():
    paths = [
        "https://www.ncei.noaa.gov/pub/data/normals/WMO/1981-2010/RA-II/Japan/NAGASAKI.csv",
        "https://www.ncei.noaa.gov/pub/data/normals/WMO/1981-2010/RA-II/Japan/TOKYO.csv"
    ]
    df = pd.concat([read_file(f) for f in paths], ignore_index=True)
    df = pd.melt(df, id_vars=["id", "type"], var_name="month")
    df["value"] = pd.to_numeric(df["value"])
    df["value"] = clean_values(df["value"], element=df["type"])
    return df


def read_file(path):
    try:
        df = pd.read_csv(path, header=None)
    except Exception as e:
        print("Exception: ", e, " at ", path)
    df = df.iloc[[22, 40, 49, 58], [0] + list(range(4, 16))]
    df.columns = ["id"] + list(range(1, 13))
    df["type"] = ["prcp", "tmax", "tmin", "tavg"]
    return df


def clean_values(x, element):
    """Clean four core element values"""
    x = x.to_numpy()
    x[element == "prcp"] = x[element == "prcp"] / 25.4
    x[element == "tmax"] = x[element == "tmax"] * 1.8 + 32
    x[element == "tmin"] = x[element == "tmin"] * 1.8 + 32
    x[element == "tavg"] = x[element == "tavg"] * 1.8 + 32
    return x
