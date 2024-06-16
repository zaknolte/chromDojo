import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch, ALL, no_update, ctx
import dash_bootstrap_components as dbc
import numpy as np
import peakutils
from scipy.signal import find_peaks

def calc_x(num_points):
    return np.linspace(0, num_points, num_points + 1)

def calc_noise(num_points, factor):
    return np.random.rand(num_points) * factor

def create_peak(x, height, center, width, skew):
    # current formula with skewness does not draw with width = 0
    # set to minimal sharp value to improve UX and not have peaks disappearing
    if width == 0:
        width = 0.1
    # https://www.desmos.com/calculator/gokr63ciym
    return height * np.exp(-0.5 * ((x - center) / (width + (skew * (x - center))))**2)
    # https://www.desmos.com/calculator/k5y9glwjee   ??
    # https://math.stackexchange.com/questions/3605861/what-is-the-graph-function-of-a-skewed-normal-distribution-curve
    # https://cremerlab.github.io/hplc-py/methodology/fitting.html

def calc_y(peaks):
    y = 0
    for peak in peaks:
        y += peak
    
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

def make_annotations(peaks, annotations_options):
    annotations = []
    for peak in peaks:
        text = ""
        for option in annotations_options:
            if option["Field"] == "Peak Name" and option["Add to Plot"]:
                text += f"{peak[0]}<br>"
            if option["Field"] == "RT" and option["Add to Plot"]:
                text += f"RT: {peak[1]}<br>"
            if option["Field"] == "Concentration" and option["Add to Plot"]:
                text += f"Conc: some conc here<br>" #TODO add integration concentrations
            if option["Field"] == "Area" and option["Add to Plot"]:
                text += f"Area: some area here<br>"
            if option["Field"] == "Height" and option["Add to Plot"]:
                text += f"RT: {peak[2]}<br>"
        annotations.append(
            {
                "text": text,
                "x": peak[1],
                "y": peak[2] * 1.02,
            }
        )
    return annotations

def integrate_peaks(x, y, width, height, threshold, distance, prominence, wlen):
    peaks = find_peaks(y, width=width, height=height, threshold=threshold, distance=distance, prominence=prominence, wlen=wlen)
    integrations = []
    for peak in range(len(peaks[1]["left_bases"])):
        start, stop = peaks[1]["left_bases"][peak], peaks[1]["right_bases"][peak]
        integrations.append(go.Scatter(x=x[start:stop], y=y[start:stop], fill="toself", mode='lines'))

    return integrations

fig = go.Figure(
        go.Scatter(
            x=[0],
            y=[0],
            mode='lines'
        ),
        layout={
            'paper_bgcolor': 'rgba(0,0,0,0)',
            "showlegend": False
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

configs = {
    "scrollZoom": True,
    "modeBarButtons": [["pan2d", "zoom2d", "drawline", "resetScale2d"]],
    "displayModeBar": True,
}

graph = dcc.Graph(figure=fig, id="main-fig", config=configs, style={"height": 800})


@callback(
    Output("main-fig", "figure"),
    Input("graph-datapoints", "value"),
    Input({'type': 'peak-edit-name', 'index': ALL}, "value"),
    Input({"type": "peak-center", "index": ALL}, "value"),
    Input({"type": "peak-height", "index": ALL}, "value"),
    Input({"type": "peak-width", "index": ALL}, "value"),
    Input({"type": "peak-skew", "index": ALL}, "value"),
    Input({"type": "peak-delete", "index": ALL}, "n_clicks"),
    Input("noise-data", "data"),
    Input("baseline-shift", "value"),
    Input({"type": "baseline-start", "index": ALL}, "value"),
    Input({"type": "baseline-stop", "index": ALL}, "value"),
    Input({"type": "baseline-slope", "index": ALL}, "value"),
    Input({"type": "reset_baseline", "index": ALL}, "value"),
    Input({"type": "trendline-delete", "index": ALL}, "n_clicks"),
    Input({"type": "bleed-start", "index": ALL}, "value"),
    Input({"type": "bleed-stop", "index": ALL}, "value"),
    Input({"type": "bleed-height", "index": ALL}, "value"),
    Input({"type": "bleed-slope", "index": ALL}, "value"),
    Input("annotations-options", "virtualRowData"), # trigger for re-arranging annotation rows
    Input("annotations-options", "cellRendererData"), # trigger for annotation checkboxes
    Input("annotations-options", "cellClicked"), # trigger for clicking a cell that contains a checkbox (cell clicks check box but don't trigger checkbox callback)
    Input("auto-integration", "checked"),
    Input("integration-width", "value"),
    Input("integration-height", "value"),
    Input("integration-threshold", "value"),
    Input("integration-distance", "value"),
    Input("integration-prominence", "value"),
    Input("integration-wlen", "value"),
    Input("main-fig", "relayoutData"), # shapes trigger relayout
    prevent_initial_call=True
)
def update_fig(
    datapoints,
    names,
    centers,
    heights,
    widths,
    skew_factor,
    delete_peak,
    noise,
    baseline_shift,
    baseline_starts,
    baseline_stops,
    slope_factors,
    reset_baseline,
    delete_trendline,
    bleed_start,
    bleed_stop,
    bleed_height,
    bleed_slope,
    annotation_order,
    add_annotation_checkbox_click,
    add_annotation_cell_click,
    auto_integrate,
    integration_width,
    integration_height,
    integration_threshold,
    integration_distance,
    integration_prominence,
    integration_wlen,
    manual_integrations
    ):
    # !! specific order of operations !!
    # some functions like bleed will overwrite some values
    # ensure data is added / manipulated to graph in correct order

    # add peaks
    x = calc_x(datapoints)
    peaks = (create_peak(x, peak[0], peak[1], peak[2], peak[3]) for peak in zip(heights, centers, widths, skew_factor))
    y = calc_y(peaks)

    # add bleed
    if all([bleed_start, bleed_stop, bleed_height, bleed_slope]):
        # have to use pattern matching callbacks since component only conditionally exists even though there's only one option
        # should always be list of single value
        y = add_bleed(y, bleed_start[0], bleed_stop[0], bleed_height[0], bleed_slope[0])

    # add baselines
    if all([baseline_starts, baseline_stops, slope_factors, reset_baseline]):
        # pattern matching callback - grabs all dynamically created baseline options
        for trendline in zip(baseline_starts, baseline_stops, slope_factors, reset_baseline):
            y = add_trendline(y, trendline[0], trendline[1], trendline[2], trendline[3])
        
    # add noise
    # if no peaks have been added yet, initialize y to zeros
    try:
        y += noise
    except TypeError:
        y = np.zeros(x.size) + noise


    # adjust full baseline
    y += baseline_shift
    
    patched_figure = Patch()

    if ctx.triggered_id == "main-fig":
        # print(manual_integrations.get("shapes"))
        # TODO add logic for integration shapes
        return no_update
    
    # add annotations
    if any([field["Add to Plot"] for field in annotation_order]):
        patched_figure["layout"]["annotations"] = make_annotations(zip(names, centers, heights), annotation_order)

    # integrate peaks
    # clear any previous integrations and re-create original peak data
    patched_figure["data"].clear()
    patched_figure["data"].append(go.Scatter(x=x, y=y))
    if auto_integrate:
        integrations = integrate_peaks(x, y, integration_width, integration_height, integration_threshold, integration_distance, integration_prominence, integration_wlen)
        patched_figure["data"].extend(integrations)

    return patched_figure
