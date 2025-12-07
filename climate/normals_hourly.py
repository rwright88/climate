"""Climate normals hourly data"""

import pandas as pd


def norm_get_hly():
    """Get all hourly climate normals data"""
    # prcp = norm_get_dly_prcp()
    # snow = norm_get_dly_snow()
    temp = norm_get_hly_temp()
    by = ["id", "month", "day", "hour"]
    # df = pd.merge(prcp, snow, how="outer", on=by)
    # df = pd.merge(df, tavg, how="outer", on=by)
    # df = pd.merge(df, tmax, how="outer", on=by)
    # df = pd.merge(df, tmin, how="outer", on=by)
    df = temp
    df = remove_invalid_dates(df)
    df = df.sort_values(by)
    return df


def norm_get_hly_temp():
    path = "https://www.ncei.noaa.gov/pub/data/normals/1981-2010/products/hourly/hly-temp-normal.txt"
    df = norm_read_hly_file(path)
    df = pd.melt(df, id_vars=["id", "month", "day"])
    df.columns = ["id", "month", "day", "hour", "temp"]
    for col in ["month", "day", "hour"]:
        df[col] = df[col].astype(int)
    df["temp"] = df["temp"] / 10
    return df


def norm_read_hly_file(path):
    """Read a normals hourly file"""
    spec1 = {"id": [(0, 11), str], "month": [(12, 14), float], "day": [(15, 17), float]}
    spec2 = {i: [(11 + i * 7, 16 + i * 7), float] for i in range(1, 25)}
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


def remove_invalid_dates(df):
    bad = (
        ((df["month"] == 2) & (df["day"] > 29))
        | ((df["month"] == 4) & (df["day"] == 31))
        | ((df["month"] == 6) & (df["day"] == 31))
        | ((df["month"] == 9) & (df["day"] == 31))
        | ((df["month"] == 11) & (df["day"] == 31))
    )
    return df[~bad]


def main():
    import matplotlib.pyplot as plt

    df = norm_get_hly()
    df = df[df["id"] == "USW00014711"]
    print(df[(df["month"] == 1) & (df["day"] == 15)])
    df1 = df[df["hour"] == 8].copy()
    df1["month_day"] = [f"{m:02}-{d:02}" for m, d in zip(df1["month"], df1["day"])]

    fig, ax = plt.subplots()
    ax.plot(df1["month_day"], df1["temp"])
    ax.grid()
    plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
