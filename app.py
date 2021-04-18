# -*- coding: utf-8 -*-
# TODO: Display something like "No data available" if nrows == 0
# TODO: Display "Loading" instead of previous figure
# TODO: Sidebar? https://github.com/facultyai/dash-bootstrap-components/tree/main/examples/multi-page-apps

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


STATIONS = read_stations("out/stations.csv")
NORM_MONTHLY = pd.read_csv("out/normals-monthly.csv")
NORM_DAILY = pd.read_csv("out/normals-daily.csv")

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

GHCN_MONTHLY_COLS = [
    {"id": "year", "name": "Year"},
    {"id": "month", "name": "Month"},
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

GHCN_DAILY_COLS = [
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

PLOTLY_CONFIG = {"displayModeBar": False}


def get_layout_plot():
    return {
        "dragmode": False,
        "height": 500,
        # "hovermode": "x",
        "margin": {"l": 75, "r": 75, "t": 75, "b": 75},
        "plot_bgcolor": "#fff",
        "showlegend": False,
        "title": {
            "font": {"size": 16},
            "x": 0.5,
            "xanchor": "center",
            "xref": "container",
            "y": 0.9,
            "yanchor": "bottom",
            "yref": "container",
        },
        "xaxis": {
            "fixedrange": True,
            "gridcolor": "#eee",
            "title": {"text": ""},
        },
        "yaxis": {
            "fixedrange": True,
            "gridcolor": "#eee",
            "title": {"text": ""},
            "zerolinecolor": "#eee",
            "zerolinewidth": 2,
        },
    }


def plot_monthly(ys, id1, title):
    """Plot normals monthly"""
    df = NORM_MONTHLY[NORM_MONTHLY["id"] == id1]
    x1 = df["month"]
    y_min = []
    y_max = []
    fig = go.Figure()
    for y in ys:
        y_max1 = df[y].max() * 1.05
        y_min.append(0 - y_max1 / 1.05 * 0.05)
        y_max.append(y_max1)
        fig.add_trace(go.Scatter(x=x1, y=df[y], connectgaps=True))
    y_min = min(y_min)
    y_max = max(y_max)
    layout = get_layout_plot()
    layout["hovermode"] = "x"
    layout["title"]["text"] = title
    # layout["yaxis"]["range"] = [y_min, y_max]
    fig.update_layout(layout)
    return fig


def plot_daily(ys, id1, title):
    """Plot normals daily"""
    df = NORM_DAILY[NORM_DAILY["id"] == id1]
    x1 = np.arange(df.shape[0])
    y_min = []
    y_max = []
    fig = go.Figure()
    for y in ys:
        y_max1 = df[y].max() * 1.05
        y_min.append(0 - y_max1 / 1.05 * 0.05)
        y_max.append(y_max1)
        fig.add_trace(go.Scatter(x=x1, y=df[y], connectgaps=True))
    y_min = min(y_min)
    y_max = max(y_max)
    layout = get_layout_plot()
    layout["hovermode"] = "x"
    layout["title"]["text"] = title
    # layout["yaxis"]["range"] = [y_min, y_max]
    fig.update_layout(layout)
    return fig


def plot_historical_yearly(df, ys, title):
    """Plot historical yearly"""
    x1 = df["year"]
    y_min = []
    y_max = []
    marker = {"color": "#1f77b4", "opacity": 0.8}
    fig = go.Figure()
    for y in ys:
        y_max1 = df[y].max() * 1.05
        y_min.append(0 - y_max1 / 1.05 * 0.05)
        y_max.append(y_max1)
        fig.add_trace(go.Scatter(x=x1, y=df[y], mode="markers", marker=marker))
    y_min = min(y_min)
    y_max = max(y_max)
    layout = get_layout_plot()
    layout["title"]["text"] = title
    # layout["yaxis"]["range"] = [y_min, y_max]
    fig.update_layout(layout)
    return fig


app = dash.Dash(
    __name__,
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

app.layout = html.Div(
    style={"max-width": 1000, "margin-left": "auto", "margin-right": "auto"},
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
        html.H2("Monthly averages"),
        html.P(
            "Climate monthly averages for 1981-2010. Precipitation and snowfall in"
            " inches. Temperature in Fahrenheit."
        ),
        dcc.Graph(id="plot-normals-monthly-temp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-normals-monthly-prcp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-normals-monthly-snow", config=PLOTLY_CONFIG),
        html.H2("Daily averages"),
        html.P(
            "Climate daily averages for 1981-2010."
            " Precipitation chance is the probability of >= 0.1 inches of rain,"
            " and snow chance is the probability of >= 0.1 inches of snow."
            " Temperature in Fahrenheit."
        ),
        dcc.Graph(id="plot-normals-daily-temp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-normals-daily-prcp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-normals-daily-snow", config=PLOTLY_CONFIG),
        html.H2("Historical yearly data"),
        html.P(
            "Historical climate data by year. Precipitation, snowfall, and snowdepth in"
            " inches. Temperature in Fahrenheit."
        ),
        dcc.Graph(id="plot-historical-yearly-temp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-historical-yearly-prcp", config=PLOTLY_CONFIG),
        dcc.Graph(id="plot-historical-yearly-snow", config=PLOTLY_CONFIG),
        html.H2("Historical monthly data"),
        html.P(
            "Historical climate data by month. Precipitation, snowfall, and snowdepth in"
            " inches. Temperature in Fahrenheit."
        ),
        dash_table.DataTable(
            id="table-ghcn-monthly",
            columns=GHCN_MONTHLY_COLS,
            filter_action="native",
            page_size=12,
            sort_action="native",
            style_header=STYLE_HEADER,
            style_cell=STYLE_CELL,
        ),
        html.H2("Historical daily data"),
        html.P(
            "Historical climate data by day. Precipitation, snowfall, and snowdepth in"
            " inches. Temperature in Fahrenheit."
        ),
        dash_table.DataTable(
            id="table-ghcn-daily",
            columns=GHCN_DAILY_COLS,
            filter_action="native",
            page_size=10,
            sort_action="native",
            style_header=STYLE_HEADER,
            style_cell=STYLE_CELL,
        ),
        html.H2("Data source"),
        html.P(
            "https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets"
        ),
        html.Div(id="intermediate-ghcn-daily", style={"display": "none"}),
        html.Div(id="intermediate-ghcn-monthly", style={"display": "none"}),
        html.Div(id="intermediate-ghcn-yearly", style={"display": "none"}),
    ],
)


@app.callback(Output("table-stations", "data"), [Input("id1", "value")])
def update_stations(id1):
    return STATIONS[STATIONS["id"] == id1].to_dict("records")


@app.callback(Output("plot-normals-monthly-temp", "figure"), [Input("id1", "value")])
def plot_normals_monthly_temp(id1):
    title = "Monthly average temperatures"
    return plot_monthly(["tmin", "tavg", "tmax"], id1=id1, title=title)


@app.callback(Output("plot-normals-monthly-prcp", "figure"), [Input("id1", "value")])
def plot_normals_monthly_prcp(id1):
    title = "Monthly average precipitation"
    return plot_monthly(["prcp"], id1=id1, title=title)


@app.callback(Output("plot-normals-monthly-snow", "figure"), [Input("id1", "value")])
def plot_normals_monthly_snow(id1):
    title = "Monthly average snowfall"
    return plot_monthly(["snow"], id1=id1, title=title)


@app.callback(Output("plot-normals-daily-temp", "figure"), [Input("id1", "value")])
def plot_normals_daily_temp(id1):
    title = "Daily average temperatures"
    return plot_daily(["tmin", "tavg", "tmax"], id1=id1, title=title)


@app.callback(Output("plot-normals-daily-prcp", "figure"), [Input("id1", "value")])
def plot_normals_daily_prcp(id1):
    title = "Daily average probability of precipitation"
    return plot_daily(["prcp"], id1=id1, title=title)


@app.callback(Output("plot-normals-daily-snow", "figure"), [Input("id1", "value")])
def plot_normals_daily_snow(id1):
    title = "Daily average probability of snowfall"
    return plot_daily(["snow"], id1=id1, title=title)


@app.callback(Output("intermediate-ghcn-daily", "children"), [Input("id1", "value")])
def get_ghcn_daily(id1):
    if id1 is None:
        return pd.DataFrame().to_json(date_format="iso", orient="split")
    df = climate.ghcn_read_dly_file(id1=id1)
    df = climate.ghcn_clean_dly_data(df)
    df = df[df["date"].dt.year >= 1950]
    # df = df.drop("id", axis=1)
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("intermediate-ghcn-monthly", "children"),
    [Input("intermediate-ghcn-daily", "children")],
)
def get_ghcn_monthly(data):
    df = pd.read_json(data, orient="split")
    df["date"] = pd.to_datetime(df["date"])
    df = climate.ghcn_calc_summary(df, freq="monthly")
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("intermediate-ghcn-yearly", "children"),
    [Input("intermediate-ghcn-daily", "children")],
)
def get_ghcn_yearly(data):
    df = pd.read_json(data, orient="split")
    df["date"] = pd.to_datetime(df["date"])
    df = climate.ghcn_calc_summary(df, freq="yearly")
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("plot-historical-yearly-temp", "figure"),
    [Input("intermediate-ghcn-yearly", "children")],
)
def plot_historical_yearly_temp(data):
    df = pd.read_json(data, orient="split")
    title = "Historical yearly temperatures"
    return plot_historical_yearly(df, ys=["tmin", "tmax"], title=title)


@app.callback(
    Output("plot-historical-yearly-prcp", "figure"),
    [Input("intermediate-ghcn-yearly", "children")],
)
def plot_historical_yearly_prcp(data):
    df = pd.read_json(data, orient="split")
    title = "Historical yearly precipitation"
    return plot_historical_yearly(df, ys=["prcp"], title=title)


@app.callback(
    Output("plot-historical-yearly-snow", "figure"),
    [Input("intermediate-ghcn-yearly", "children")],
)
def plot_historical_yearly_snow(data):
    df = pd.read_json(data, orient="split")
    title = "Historical yearly snowfall"
    return plot_historical_yearly(df, ys=["snow"], title=title)


@app.callback(
    Output("table-ghcn-monthly", "data"),
    [Input("intermediate-ghcn-monthly", "children")],
)
def table_ghcn_monthly(data):
    df = pd.read_json(data, orient="split")
    return df.to_dict("records")


@app.callback(
    Output("table-ghcn-daily", "data"),
    [Input("intermediate-ghcn-daily", "children")],
)
def table_ghcn_daily(data):
    df = pd.read_json(data, orient="split")
    df = df.sort_values("date", ascending=False)
    df["date"] = df["date"].astype(str)
    return df.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
