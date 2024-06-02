import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch, ALL, no_update
import dash_bootstrap_components as dbc
import numpy as np
import peakutils
from scipy.stats import skewnorm #add skewness to peaks

def calc_x(num_points):
    return np.linspace(0, num_points, num_points + 1)

def calc_noise(num_points, factor):
    return np.random.rand(num_points) * factor

def create_peak(x, height, center, width):
    return peakutils.gaussian(x, height, center, width)

def calc_y(peaks, noise):
    y = noise
    for peak in peaks:
        y += peak
    
    return y


fig = go.Figure(
        go.Scatter(
            x=[0],
            y=[0],
        ),
        layout={
            'paper_bgcolor': 'rgba(0,0,0,0)',
        },
)

fig.update_xaxes(
    {
        "color": "white",
        "title": {
            "text": "Time",
        },
        "showgrid": False
    },
)

fig.update_yaxes(
    {
        "color": "white",
        "title": {
            "text": "Intensity",
        },
        "showgrid": False
    }
)

graph = dcc.Graph(figure=fig, className='content', id="main-fig")


@callback(
    Output("main-fig", "figure"),
    Input("graph-datapoints", "value"),
    Input({"type": "peak-center", "index": ALL}, "value"),
    Input({"type": "peak-height", "index": ALL}, "value"),
    Input({"type": "peak-width", "index": ALL}, "value"),
    Input("add-noise", "value"),
    State({'type': 'peak-edit-name', 'index': ALL}, "value"),
    Input({'type': 'peak-add-annotation', 'index': ALL}, "value"),
    prevent_initial_call=True
)
def update_fig(datapoints, centers, heights, widths, noise, names, is_checked):
    if not all([datapoints, centers, heights, widths, noise, is_checked]):
        return no_update
    
    patched_figure = Patch()

    x = calc_x(datapoints)
    peaks = (create_peak(x, peak[0], peak[1], peak[2]) for peak in zip(heights, centers, widths))
    y = calc_y(peaks, calc_noise(x.size, noise))

    patched_figure["data"][0]["x"] = x
    patched_figure["data"][0]["y"] = y
    
    annotations = [
        {
            "text": values[1],
            "x": values[2],
            "y": values[3],
        }
        for values in zip(is_checked, names, centers, heights) if values[0]
    ]
    patched_figure["layout"]["annotations"] = annotations

    return patched_figure
