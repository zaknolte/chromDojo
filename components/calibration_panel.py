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


calibration_panel = dmc.TabsPanel(
    html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(id="peak-calibration-selection", clearable=False, className="dark-dropdown"),
                    html.Div(
                        [
                            dbc.Button("Add Calibrator", color="success", className="me-1", style={"width": "100%"}),
                            dag.AgGrid(
                                id="calibration-table",
                                columnDefs=[
                                    {
                                        "field": "Calibrator",
                                        "width": 100,
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
                                    },
                                    {
                                        "field": "Abundance",
                                        "width": 100,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                    },
                                    {
                                        "field": "Use",
                                        "width": 90,
                                        "resizable": False,
                                        "sortable": False,
                                        "suppressMovable": True,
                                        "cellRenderer": "Checkbox",
                                        "cellStyle": {"textAlign": "center"}
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