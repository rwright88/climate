# -*- coding: utf-8 -*-

from datetime import date

from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import climate


def read_stations(path):
    df = pd.read_csv(path)
    df = df[df["wmo_id"].notna()]
    df["name"] = df["name"].str.lower()
    df = df.sort_values("name")
    return df


def read_normals(path):
    df = pd.read_csv(path)
    return df


STATIONS = read_stations("../data/climate/stations/stations.csv")
NORM = read_normals("../data/climate/normals/normals.csv")

NAMES = [
    {"label": name, "value": id1} for name, id1 in zip(STATIONS["name"], STATIONS["id"])
]
INITIAL = "USW00094728"

STYLE_HEADER = {"fontWeight": "bold"}
STYLE_CELL = {"font-family": "Arial", "font-size": 14, "padding": 10}

STATIONS_COLS = [
    {"id": "id", "name": "ID"},
    {"id": "latitude", "name": "Latitude"},
    {"id": "longitude", "name": "Longitude"},
    {"id": "elevation", "name": "Elevation"},
    {"id": "state", "name": "State"},
    {"id": "name", "name": "Name"},
    {"id": "gsn_flag", "name": "GSN Flag"},
    {"id": "hcn_flag", "name": "HCN Flag"},
    {"id": "wmo_id", "name": "WMO ID"},
]

NORM_COLS = [
    {"id": "month", "name": "Month", "type": "numeric"},
    {
        "id": "prcp",
        "name": "Precipitation",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "id": "snow",
        "name": "Snowfall",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "tavg",
        "name": "Temp avg",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "tmax",
        "name": "Temp max",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "tmin",
        "name": "Temp min",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
]

GHCN_COLS = [
    {"id": "date", "name": "Date"},
    {
        "id": "prcp",
        "name": "Precipitation",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "id": "snow",
        "name": "Snowfall",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "snwd",
        "name": "Snow depth",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "tmax",
        "name": "Temp max",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
    {
        "id": "tmin",
        "name": "Temp min",
        "type": "numeric",
        "format": Format(precision=1, scheme=Scheme.fixed),
    },
]

app = dash.Dash(
    __name__,
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

app.layout = html.Div(
    style={"max-width": 900, "margin-left": "auto", "margin-right": "auto"},
    children=[
        html.H1("Climate data"),
        html.Label("Choose a station:"),
        dcc.Dropdown(
            id="id1",
            options=NAMES,
            # value=INITIAL,
            placeholder="Select a station",
            style={"margin-top": "5px"},
        ),
        html.H2("Station metadata"),
        dash_table.DataTable(
            id="table-stations",
            columns=STATIONS_COLS,
            style_header=STYLE_HEADER,
            style_cell=STYLE_CELL,
        ),
        html.H2("Monthly normals"),
        html.P(
            "Climate monthly averages for 1981-2010. Precipitation and snowfall in"
            " inches. Temperature in Fahrenheit."
        ),
        dash_table.DataTable(
            id="table-normals",
            columns=NORM_COLS,
            style_header=STYLE_HEADER,
            style_cell=STYLE_CELL,
        ),
        html.H2("Daily normals"),
        html.P("TODO"),
        html.H2("Historical daily data"),
        html.P(
            "Historical climate data by day. Precipitation, snowfall, and snowdepth in"
            " inches. Temperature in Fahrenheit."
        ),
        html.P(
            "Note: This table can take 5+ seconds to update because it downloads data"
            " from an outside source."
        ),
        dash_table.DataTable(
            id="table-ghcn",
            columns=GHCN_COLS,
            filter_action="native",
            page_size=10,
            sort_action="native",
            style_header=STYLE_HEADER,
            style_cell=STYLE_CELL,
        ),
        html.H2("Data source"),
        html.P("https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets")
    ],
)


@app.callback(Output("table-stations", "data"), [Input("id1", "value")])
def update_stations(id1):
    return STATIONS[STATIONS["id"] == id1].to_dict("records")


@app.callback(Output("table-normals", "data"), [Input("id1", "value")])
def update_normals(id1):
    df = NORM[NORM["id"] == id1]
    df = df.drop("id", axis=1)
    return df.to_dict("records")


@app.callback(Output("table-ghcn", "data"), [Input("id1", "value")])
def get_ghcn(id1):
    if id1 is None:
        return pd.DataFrame().to_dict("records")
    df = climate.ghcn_read_dly_file(id1=id1)
    df = climate.ghcn_clean_dly_data(df)
    df = df.drop("id", axis=1)
    df = df.sort_values("date", ascending=False)
    df["date"] = df["date"].astype(str)
    return df.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
