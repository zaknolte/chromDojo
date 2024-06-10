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

def create_peak(x, height, center, width, skew):
    # return peakutils.gaussian(x, height, center, width)
    # https://www.desmos.com/calculator/gokr63ciym
    return height * np.exp(-0.5 * ((x - center) / (width + (skew * (x - center))))**2)
    # https://www.desmos.com/calculator/k5y9glwjee   ??
    # https://math.stackexchange.com/questions/3605861/what-is-the-graph-function-of-a-skewed-normal-distribution-curve

def calc_y(peaks):
    y = 0
    for peak in peaks:
        y += peak
    
    return y

def add_noise(y, noise):
    y += noise
    return y

def add_trendline(y, start, stop, factor, reset):
    if factor != 0:
        y_slice = y[start:stop]
        for i in range(len(y_slice)):
            y_slice[i] += (i * factor)
        
        y[start: stop] = y_slice

        if not reset:
            y[stop:] = y_slice[-1]

    return y

def add_bleed(y, start, stop, height, factor):
    x = calc_x(stop - start) # x range to replace with slope
    x -= x[len(x)//2] # shift range to center on 0 for sigmoid
    vals = height / (1 + np.exp(-x*factor) / factor)

    y[start: stop + 1] += vals
    y[stop + 1:] += vals[-1]

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
    State({'type': 'peak-edit-name', 'index': ALL}, "value"),
    Input({'type': 'peak-add-annotation', 'index': ALL}, "value"),
    Input({"type": "peak-center", "index": ALL}, "value"),
    Input({"type": "peak-height", "index": ALL}, "value"),
    Input({"type": "peak-width", "index": ALL}, "value"),
    Input({"type": "peak-skew", "index": ALL}, "value"),
    Input("add-noise", "value"),
    Input("baseline-shift", "value"),
    Input({"type": "baseline-start", "index": ALL}, "value"),
    Input({"type": "baseline-stop", "index": ALL}, "value"),
    Input({"type": "baseline-slope", "index": ALL}, "value"),
    Input({"type": "reset_baseline", "index": ALL}, "value"),
    Input({"type": "bleed-start", "index": ALL}, "value"),
    Input({"type": "bleed-stop", "index": ALL}, "value"),
    Input({"type": "bleed-height", "index": ALL}, "value"),
    Input({"type": "bleed-slope", "index": ALL}, "value"),
    prevent_initial_call=True
)
def update_fig(
    datapoints,
    names,
    add_annotation,
    centers,
    heights,
    widths,
    skew_factor,
    noise,
    baseline_shift,
    baseline_starts,
    baseline_stops,
    slope_factors,
    reset_baseline,
    bleed_start,
    bleed_stop,
    bleed_height,
    bleed_slope
    ):
    # early return if no peak data yet
    if not all([datapoints, centers, heights, widths, skew_factor, add_annotation]):
        return no_update
    
    patched_figure = Patch()

    # add peaks
    x = calc_x(datapoints)
    peaks = (create_peak(x, peak[0], peak[1], peak[2], peak[3]) for peak in zip(heights, centers, widths, skew_factor))
    y = calc_y(peaks)

    # add bleed
    if all([bleed_start, bleed_stop, bleed_height, bleed_slope]):
        # have to use pattern matching callbacks since component only conditionally exists even though there's only one option
        # should always be lists of single value
        y = add_bleed(y, bleed_start[0], bleed_stop[0], bleed_height[0], bleed_slope[0])

    # add baselines
    if all([baseline_starts, baseline_stops, slope_factors, reset_baseline]):
        # pattern matching callback - grabs all dynamically created baseline options
        for trendline in zip(baseline_starts, baseline_stops, slope_factors, reset_baseline):
            y = add_trendline(y, trendline[0], trendline[1], trendline[2], trendline[3])
        
    # add noise last otherwise some functions will ovewrite
    noise = calc_noise(x.size, noise)
    y = add_noise(y, noise)

    # adjust full baseline
    y += baseline_shift
    
    annotations = [
        {
            "text": values[1],
            "x": values[2],
            "y": values[3],
        }
        for values in zip(add_annotation, names, centers, heights) if values[0]
    ]
    patched_figure["layout"]["annotations"] = annotations

    patched_figure["data"][0]["x"] = x
    patched_figure["data"][0]["y"] = y

    return patched_figure
