from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import peakutils
from scipy.signal import find_peaks
import jsonpickle

data_tab = html.Div(
    [
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab("Results", value="results"),
                        dmc.TabsTab("Calibration Curves", value="curves"),
                    ],
                    justify="center"
                ),
                dmc.TabsPanel(
                    dag.AgGrid(
                            id="results-table",
                            columnDefs=[
                                {
                                    "field": "RT",
                                    "width": 140,
                                },
                                {
                                    "field": "Name",
                                    "width": 140,
                                },
                                {
                                    "field": "Height",
                                    "width": 140,
                                },
                                {
                                    "field": "Area",
                                    "width": 140,
                                },
                                {
                                    "field": "Concentration",
                                    "width": 140,
                                },
                                {
                                    "field": "Units",
                                    "width": 140,
                                },
                            ],
                            dashGridOptions={
                                "animateRows": True,
                                },
                            style={"width": None, "height": 500},
                            className="ag-theme-balham-dark"
                        ),
                        value="results"
                ),
                dmc.TabsPanel("curve data here", value="curves"),
            ],
            value="results",
            color="red",
            style={"width": "60%"}
        ),
    ],
    style={"display": "flex", "justifyContent": "center"}
)

@callback(
    Output("results-table", "rowData"),
    Input("x-y-data", "data"),
    prevent_initial_call=True
)
def update_results_table(graph_data):
    if graph_data is not None and any(graph_data["y"]):
        peaks = jsonpickle.decode(graph_data["peaks"])
        row_data = []

        for peak in peaks:
            row_data.append(
                {
                    "RT": f"{peak.center:.2f} min",
                    "Name": peak.name,
                    "Height": f"{peak.height:.2f}",
                    "Area": f"{peak.area:.2f}",
                    "Concentration": "N/A",
                    "Units": "N/A"
                }
            )

        return row_data
    
    return no_update