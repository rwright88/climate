"""Create climate datasets"""

import os

import numpy as np
import pandas as pd

import climate

OUT_DIR = "out"


def main():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR, exist_ok=True)

    stations = climate.ghcn_read_stations_file()
    normals_monthly = climate.norm_get_mly()
    normals_daily = climate.norm_get_dly()

    stations.to_csv(os.path.join(OUT_DIR, "stations.csv"), index=False)
    normals_monthly.to_csv(os.path.join(OUT_DIR, "normals-monthly.csv"), index=False)
    normals_daily.to_csv(os.path.join(OUT_DIR, "normals-daily.csv"), index=False)

    df = climate.ghcn_read_dly_file(id1="USW00094728")
    df = climate.ghcn_clean_dly_data(df)
    print(df)
    print(climate.ghcn_calc_summary(df, freq="yearly"))
    print(climate.ghcn_calc_summary(df, freq="monthly"))


if __name__ == "__main__":
    main()

