import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch, ALL, no_update, ctx
import dash_bootstrap_components as dbc
import numpy as np
import peakutils
from scipy.signal import find_peaks
from components.Compound import Compound
import jsonpickle

def calc_x(num_points):
    return np.linspace(0, num_points, num_points + 1) / 60

def calc_noise(num_points, factor):
    return np.random.rand(num_points) * factor

def calc_y(peaks):
    y = 0
    for peak in peaks:
        y += peak.y
    
    return y

def add_trendline(y, start, stop, factor, reset):
    if factor != 0:
        y_slice = y[start:stop]
        for i in range(len(y_slice)):
            y_slice[i] += (i * factor)
        
        y[start: stop] += y_slice

        if not reset:
            y[stop:] += y_slice[-1]

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
                text += f"{peak.name}<br>"
            if option["Field"] == "RT" and option["Add to Plot"]:
                text += f"RT: {peak.center:.2f} min<br>"
            if option["Field"] == "Concentration" and option["Add to Plot"]:
                text += f"Conc: {peak.calibration.calculate_concentration(peak.area):.2f} {peak.calibration.units}<br>" #TODO add integration concentrations
            if option["Field"] == "Area" and option["Add to Plot"]:
                text += f"Area: {peak.area:.2f}<br>"
            if option["Field"] == "Height" and option["Add to Plot"]:
                text += f"Height: {peak.height:.2f}<br>"
        annotations.append(
            {
                "text": text,
                "x": peak.center,
                "y": peak.height * 1.04,
            }
        )

    return annotations

def integrate_peaks(peak_list, x, y, width, height, threshold, distance, prominence, wlen):
    peaks = find_peaks(y, width=width, height=height, threshold=threshold, distance=distance, prominence=prominence, wlen=wlen)
    integrations = []
    baseline = peakutils.baseline(y)
    for i in range(len(peaks[1]["left_bases"])):
        for peak in peak_list:
            if peak.center == peaks[0][i] / 60:
                start, stop = peaks[1]["left_bases"][i], peaks[1]["right_bases"][i]
                auc = np.trapz(y[start:stop], x[start:stop]) - np.trapz(baseline[start:stop], x[start:stop])
                peak.start_idx = start
                peak.stop_idx = stop
                peak.area = auc
        integrations.append(go.Scatter(x=x[start:stop], y=y[start:stop], fill="toself", mode='lines'))

    return integrations

def update_peaks(peak_data, x, names, heights, centers, widths, skew_factor):
    current_peaks = jsonpickle.decode(peak_data["peaks"])
    all_peaks = [Compound(peak[0], x, peak[1], peak[2], peak[3], peak[4]) for peak in zip(names, heights, centers, widths, skew_factor)]
    names = [i.name for i in current_peaks]
    try:
        # make sure to update the name of the peak if it is edited to avoid adding a copy of it
        if ctx.triggered_id["type"] == "peak-edit-name":
            names = [ctx.inputs[i] for i in ctx.inputs if "peak-edit-name" in i]
            for peak, name in zip(current_peaks, names):
                peak.name = name
            return current_peaks
    except TypeError:
        pass

    for peak in all_peaks:
        # add new peak if it doesn't exist yet
        if peak.name not in names:
            current_peaks.append(peak)
        else:
            # remove any current peaks that have been deleted
            current_peaks = [c for c in current_peaks if c.name in [a.name for a in all_peaks]]
            # just update values if it already exists
            # make sure not to overwrite any existing calibration data
            for curr in current_peaks:
                if curr.name == peak.name:
                    curr.name = peak.name
                    curr.x = x
                    curr.height = peak.height
                    curr.center = peak.center
                    curr.width = peak.width
                    curr.skew = peak.skew
                    curr.y = curr.create_peak()

    return current_peaks

fig = go.Figure(
        go.Scatter(
            x=[0],
            y=[0],
            mode='lines'
        ),
        layout={
            'paper_bgcolor': 'rgba(0,0,0,0)',
            "showlegend": False,
            "xaxis": {
                "color": "white",
                "title": {
                    "text": "Time",
                },
                "showgrid": False
            },
            "yaxis": {
                "color": "white",
                "title": {
                    "text": "Abundance",
                },
                "showgrid": False
            }
        },
)

configs = {
    "scrollZoom": True,
    "modeBarButtons": [["pan2d", "zoom2d", "drawline", "resetScale2d"]],
    "displayModeBar": True,
}

graph = dcc.Graph(
    figure=fig, 
    id="main-fig", 
    config=configs, 
    style={"height": 800}
)


@callback(
    Output("main-fig", "figure"),
    Output("x-y-data", "data"),
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
    State("x-y-data", "data"),
    Input("table-updates", "data"), # make sure to update fig after minor updates to cals / results table
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
    manual_integrations,
    peak_data,
    table_updates
    ):
    # !! specific order of operations !!
    # some functions like bleed will overwrite some values
    # ensure data is added / manipulated to graph in correct order

    # add peaks
    x = calc_x(datapoints)
    if peak_data is not None:
        # make sure to just update peak if it already exists
        # otherwise it will be overwritten with a new instance
        peak_list = update_peaks(peak_data, x, names, heights, centers, widths, skew_factor)
    else:
        peak_list = [Compound(peak[0], x, peak[1], peak[2], peak[3], peak[4]) for peak in zip(names, heights, centers, widths, skew_factor)]

    y = calc_y(peak_list)

    # add bleed
    if all([bleed_start, bleed_stop, bleed_height, bleed_slope]):
        # have to use pattern matching callbacks since component only conditionally exists even though there's only one option
        # should always be list of single value
        y = add_bleed(y, bleed_start[0] * 60, bleed_stop[0] * 60, bleed_height[0], bleed_slope[0] * 60)

    # add baselines
    if all([baseline_starts, baseline_stops, slope_factors, reset_baseline]):
        # pattern matching callback - grabs all dynamically created baseline options
        for trendline in zip(baseline_starts, baseline_stops, slope_factors, reset_baseline):
            y = add_trendline(y, trendline[0] * 60, trendline[1] * 60, trendline[2] / 60, trendline[3])
        
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

    # integrate peaks
    # clear any previous integrations and re-create original peak data
    patched_figure["data"].clear()
    patched_figure["data"].append(go.Scatter(x=x, y=y))
    if auto_integrate:
        integrations = integrate_peaks(peak_list, x, y, integration_width, integration_height, integration_threshold, integration_distance, integration_prominence, integration_wlen)
        patched_figure["data"].extend(integrations)
    else:
        for peak in peak_list:
            peak.clear_integration()
    
    # add annotations
    if annotation_order is not None and any([field["Add to Plot"] for field in annotation_order]):
        patched_figure["layout"]["annotations"] = make_annotations(peak_list, annotation_order)

    # dcc.Store can't store raw python objects
    # json serialize first then deserialize when needed to access peaks
    return patched_figure, {"x": x, "y": y, "peaks": jsonpickle.encode(peak_list)}
