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

OUT_NORMALS = "../data/climate/normals/normals.csv"
OUT_STATIONS = "../data/climate/stations/stations.csv"


def main():
    # First, get static normals data if we don't already have it
    # For now, also assume that stations metadata is static

    if not os.path.isdir(os.path.dirname(OUT_NORMALS)):
        os.makedirs(os.path.dirname(OUT_NORMALS), exist_ok=True)

    if not os.path.exists(OUT_NORMALS):
        normals = climate.norm_get_mly()
        normals.to_csv(OUT_NORMALS, index=False)

    if not os.path.isdir(os.path.dirname(OUT_STATIONS)):
        os.makedirs(os.path.dirname(OUT_STATIONS), exist_ok=True)

    if not os.path.exists(OUT_STATIONS):
        stations = climate.ghcn_read_stations_file()
        stations.to_csv(OUT_STATIONS, index=False)


if __name__ == "__main__":
    main()

