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
                    }
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
    Input("calibration-table", "cellValueChanged"),
    Input("calibration-table", "cellRendererData"),
    State("peak-calibration-selection", "value"),
    State("x-y-data", "data"),
    prevent_initial_call=True,
)
def delete_calibrator(new_data, row_data, compound, peak_data):
    rows = no_update
    peaks = jsonpickle.decode(peak_data["peaks"])
    # cellRendererData ctx is the delete button
    if ctx.triggered[0]["prop_id"] == "calibration-table.cellRendererData":
        if peak_data:
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
    patched_fig = Patch()
    for peak in peaks:
        if peak.name == compound:
            traces = []
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
                else:
                    marker = {
                        "symbol": "circle-open",
                        "line": {
                            "color": "rgb(0, 0, 0)"
                        },
                        "color": "rgb(50, 50, 50)"
                    }

                traces.append(go.Scatter(x=[cal.x], y=[cal.y], mode="markers", marker=marker))
                
            patched_fig["data"] = traces
    
    return patched_fig, rows, {"x": peak_data["x"], "y": peak_data["y"], "peaks": jsonpickle.encode(peaks)}