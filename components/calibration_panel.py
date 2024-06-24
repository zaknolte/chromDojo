import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import peakutils
from scipy.signal import find_peaks
import jsonpickle
import datetime

from components.Calibration import calPoint


calibration_panel = dmc.TabsPanel(
    html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(id="peak-calibration-selection", clearable=False, className="dark-dropdown"),
                    html.Div(
                        [
                            dbc.Button("Add Calibrator", id="add-cal", color="success", className="me-1", style={"width": "100%"}, disabled=True),
                            dag.AgGrid(
                                id="calibration-table",
                                columnDefs=[
                                    {
                                        "field": "Level",
                                        "width": 80,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                    },
                                    {
                                        "field": "Concentration",
                                        "width": 100,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                        'editable': True,
                                        'cellStyle': {
                                            "display": "flex",
                                            "justifyContent": "end"
                                        }
                                    },
                                    {
                                        "field": "Abundance",
                                        "width": 100,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                        'editable': True,
                                        'cellStyle': {
                                            "display": "flex",
                                            "justifyContent": "end"
                                        }
                                    },
                                    {
                                        "field": "Use",
                                        "width": 45,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                        "cellRenderer": "Checkbox",
                                        "cellStyle": {"textAlign": "center"}
                                    },
                                    {
                                        "field": "Delete",
                                        "width": 70,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                        "cellRenderer": "deleteCal",
                                        "cellRendererParams": {
                                            "variant": "subtle",
                                            "icon": "material-symbols-light:cancel-outline",
                                            "color": "red",
                                        },
                                        'cellStyle': {
                                            "display": "flex",
                                            "alignItems": "center"
                                        }
                                    },
                                ],
                                style={"width": 400, "height": 400},
                                className="ag-theme-balham-dark"
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dmc.Select(
                                id="regression-select",
                                label="Regression",
                                value="linear",
                                data=[
                                    {"value": "linear", "label": "Linear"},
                                    {"value": "quadratic", "label": "Quadratic"},
                                    {"value": "response-factor", "label": "Response Factor"},
                                ],
                            ),
                            dmc.Select(
                                id="weight-select",
                                label="Weighting",
                                value="none",
                                data=[
                                    {"value": "none", "label": "None"},
                                    {"value": "1x", "label": "1/x"},
                                    {"value": "1x2", "label": "1/x^2"},
                                    {"value": "1y", "label": "1/y"},
                                    {"value": "1y2", "label": "1/y^2"},
                                ],
                            ),
                        ],
                        style={"display": "flex", "justifyContent": "space-evenly", "z-index": -1, "margin-bottom": "-10%"}
                    ),
                    dcc.Graph(
                        figure=go.Figure(
                            go.Scatter(
                                x=[0],
                                y=[0]
                            ),
                            layout={
                                'paper_bgcolor': 'rgba(0,0,0,0)',
                                "showlegend": False,
                                "xaxis": {
                                    "color": "white",
                                    "title": {
                                        "text": "Concentration"
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
                        ),
                        id="calibration-curve",
                        config={
                            "displayModeBar": False,
                            "staticPlot": True
                        },
                        style={"height": 550}
                    )
                ]
            )
        ],
        style={"display": "flex"}
    ),
    value="curves"
)

@callback(
    Output("peak-calibration-selection", "options"),
    Input("add-peak", "n_clicks"),
    Input({'type': 'peak-edit-name', 'index': ALL}, "value"),
    prevent_initial_call=True
)
def add_curve_options(new_peak, edited_peak):
    return [peak for peak in edited_peak]

@callback(
    Output("calibration-table", "rowData"),
    Output("add-cal", "disabled"),
    Input("peak-calibration-selection", "value"),
    State("x-y-data", "data"),
    prevent_initial_call=True
)
def display_curve(compound, peak_data):
    if peak_data:
        row_data = []
        peaks = jsonpickle.decode(peak_data["peaks"])
        for peak in peaks:
            if peak.name == compound:
                for cal in peak.calibration.points:
                    row_data.append(
                        {
                            "Level": cal.name,
                            "Concentration": cal.x,
                            "Abundance": cal.y,
                            "Use": cal.used,
                            "Delete": "X"
                        }
                    )
        
        return row_data, False
    
    return no_update, no_update

@callback(
    Output("calibration-table", "rowData", allow_duplicate=True),
    Output("x-y-data", "data", allow_duplicate=True),
    Input("add-cal", "n_clicks"),
    State("peak-calibration-selection", "value"),
    State("x-y-data", "data"),
    prevent_initial_call=True,
)
def add_calibrator(n_clicks, compound, peak_data):
    if peak_data:
        peaks = jsonpickle.decode(peak_data["peaks"])
        patched_table = Patch()
        for peak in peaks:
            if peak.name == compound:
                name = len(peak.calibration.points) + 1
                x = 0
                y = 0

                row_data = {
                        "Level": name,
                        "Concentration": x,
                        "Abundance": y,
                        "Use": True,
                        "Delete": "X"
                    }
                patched_table.append(row_data)

                peak.calibration.add_point(calPoint(name, x, y))

                return patched_table, {"x": peak_data["x"], "y": peak_data["y"], "peaks": jsonpickle.encode(peaks)}
    
    return no_update

@callback(
    Output("calibration-curve", "figure"),
    Output("calibration-table", "rowData", allow_duplicate=True),
    Output("x-y-data", "data", allow_duplicate=True),
    Output("table-updates", "data", allow_duplicate=True),
    Input("calibration-table", "cellValueChanged"),
    Input("calibration-table", "cellRendererData"),
    Input("regression-select", "value"),
    Input("weight-select", "value"),
    State("peak-calibration-selection", "value"),
    State("x-y-data", "data"),
    prevent_initial_call=True,
)
def update_calibrators(new_data, row_data, regression_type, weighting, compound, peak_data):
    def get_r_squared(coefs):
        fit = np.poly1d(coefs)
        yhat = fit(x)
        ybar = np.sum(y)/len(y)
        ssreg = np.sum((yhat-ybar)**2)
        sstot = np.sum((y - ybar)**2)
        return ssreg / sstot
    
    rows = no_update
    peaks = jsonpickle.decode(peak_data["peaks"])
    # cellRendererData ctx is the delete button
    if ctx.triggered[0]["prop_id"] == "calibration-table.cellRendererData":
        for peak in peaks:
            if peak.name == compound:
                peak.calibration.delete_point(int(row_data["rowIndex"]) + 1)
                peak.calibration.rename_points()

                rows = []
                for cal in peak.calibration.points:
                    rows.append(
                        {
                            "Level": cal.name,
                            "Concentration": cal.x,
                            "Abundance": cal.y,
                            "Use": cal.used,
                            "Delete": "X"
                        }
                    )

    # create the cal curve graph when updating points or switching compounds
    patched_fig = Patch()
    for peak in peaks:
        if peak.name == compound:
            traces = []
            x = []
            y = []
            # build cal points
            for cal in peak.calibration.points:
                if cal.name == new_data[0]["data"]["Level"]:
                    cal.x = new_data[0]["data"]["Concentration"]
                    cal.y = new_data[0]["data"]["Abundance"]
                    cal.set_used(new_data[0]["data"]["Use"])

                if cal.used:
                    marker = {
                        "symbol": "circle",
                        "line": {
                            "color": "rgb(0, 0, 0)"
                        },
                        "color": "rgb(50, 50, 50)"
                    }
                    x.append(cal.x)
                    y.append(cal.y)
                else:
                    marker = {
                        "symbol": "circle-open",
                        "line": {
                            "color": "rgb(0, 0, 0)"
                        },
                        "color": "rgb(50, 50, 50)"
                    }

                traces.append(go.Scatter(x=[cal.x], y=[cal.y], mode="markers", marker=marker))

            
            text = ""
            x = np.asarray(x)
            y = np.asarray(y)

            weights = {
                "none": None,
                "1x": 1 / x,
                "1x2": 1 / (x * x),
                "1y": 1 / y,
                "1y2": 1 / (y * y),
            }

            w = weights[weighting]
            # build curves
            if regression_type == "linear":
                coefs = np.polyfit(x, y, 1)
                # add additional points to plot a smoother curve
                x = np.linspace(np.min(x), np.max(x), 20)
                r2 = get_r_squared(coefs)

                y_fit = coefs[0] * x + coefs[1]

                const_sign = "+" if coefs[1] > 0 else ""

                text += f"{coefs[0]:.4g}x {const_sign} {coefs[1]:.4g}"

            elif regression_type == "quadratic":
                coefs = np.polyfit(x, y, 2)
                r2 = get_r_squared(coefs)
                # add additional points to plot a smoother curve
                x = np.linspace(np.min(x), np.max(x), 20)
                y_fit = (coefs[0] * x * x) + (coefs[1] * x) + coefs[2]

                slope_sign = "+" if coefs[1] > 0 else ""
                const_sign = "+" if coefs[2] > 0 else ""

                text += f"{coefs[0]:.4g}x^2 {slope_sign} {coefs[1]:.4g}x {const_sign} {coefs[2]:.4g}"

            elif regression_type == "response-factor":
                if "x" in weighting:
                    pass 
                coefs = np.linalg.lstsq(np.asarray(x).reshape(-1,1), y)[0]
                # add additional points to plot a smoother curve
                x = np.linspace(np.min(x), np.max(x), 20)
                r2 = get_r_squared(coefs)
                y_fit = x * coefs[0]

                text += f"{coefs[0]:.4g}x"
            
            peak.calibration.type = regression_type
            peak.calibration.weighting = weighting
            peak.calibration.coefficients = coefs

            if regression_type != "response-factor":
                text += f"<br>r2 = {r2:.5f}"

            annotation = [
                {
                    "text": text,
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.07,
                    "y": 0.95,
                    "showarrow": False,
                    "textfont": {
                        "color": "darkgrey"
                    }
                }
            ]

            traces.append(
                go.Scatter(
                    x=x,
                    y=y_fit,
                    mode="lines",
                    marker={"color": "darkgrey"},
                )
            )

            patched_fig["layout"]["annotations"] = annotation
            patched_fig["layout"]["xaxis"]["title"]["text"] = f"Concentration ({peak.calibration.units})"
            patched_fig["data"] = traces
    
    return patched_fig, rows, {"x": peak_data["x"], "y": peak_data["y"], "peaks": jsonpickle.encode(peaks)}, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
