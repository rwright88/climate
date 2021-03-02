"""Create or get climate datasets

Types of datasets:

- Station meta data
- Monthly normals
- Daily normals
- Historical monthly/yearly data?
- Historical daily data
"""

import os

import numpy as np
import pandas as pd

from climate.utils import profile
import climate

OUT_STATIONS = "out/stations.csv"
OUT_NORMALS_MONTHLY = "out/normals-monthly.csv"
OUT_NORMALS_DAILY = "out/normals-daily.csv"


def main():
    for out in [OUT_STATIONS, OUT_NORMALS_MONTHLY, OUT_NORMALS_DAILY]:
        if not os.path.isdir(os.path.dirname(out)):
            os.makedirs(os.path.dirname(out), exist_ok=True)

    if not os.path.exists(OUT_STATIONS):
        climate.ghcn_read_stations_file().to_csv(OUT_STATIONS, index=False)

    if not os.path.exists(OUT_NORMALS_MONTHLY):
        climate.norm_get_mly().to_csv(OUT_NORMALS_MONTHLY, index=False)

    if not os.path.exists(OUT_NORMALS_DAILY):
        climate.norm_get_dly().to_csv(OUT_NORMALS_DAILY, index=False)

    # TODO: Temp
    stations = climate.ghcn_read_stations_file()
    df = climate.ghcn_clean_dly_data(climate.ghcn_read_dly_file(id1="USW00013739"))
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    agg = {"prcp": "sum", "snow": "sum", "snwd": "mean", "tmax": "mean", "tmin": "mean"}
    df.groupby(["year"]).agg(agg).reset_index()
    df.groupby(["year", "month"]).agg(agg).reset_index()


if __name__ == "__main__":
    main()

