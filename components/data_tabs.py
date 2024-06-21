from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import peakutils
from scipy.signal import find_peaks

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
    Input({'type': 'peak-edit-name', 'index': ALL}, "value"),
    State({"type": "peak-center", "index": ALL}, "value"),
    State("auto-integration", "checked"),
    State("integration-width", "value"),
    State("integration-height", "value"),
    State("integration-threshold", "value"),
    State("integration-distance", "value"),
    State("integration-prominence", "value"),
    State("integration-wlen", "value"),
    prevent_initial_call=True
)
def update_results_table(graph_data, peak_names, centers, integrations, width, height, threshold, distance, prominence, wlen):
    if graph_data["y"]:
        y = np.asarray(graph_data["y"])
        row_data = []
        baseline = peakutils.baseline(y)
        peaks = find_peaks(y, width=width, height=height, threshold=threshold, distance=distance, prominence=prominence, wlen=wlen)[1]

        for i in range(len(peaks["left_bases"])):
            start, stop = peaks["left_bases"][i], peaks["right_bases"][i]
            auc = 0
            if integrations:
                auc = np.trapz(y[start:stop], graph_data["x"][start:stop]) - np.trapz(baseline[start:stop], graph_data["x"][start:stop])
            row_data.append(
                {
                    "RT": f"{centers[i]} min",
                    "Name": peak_names[i],
                    "Height": peaks["peak_heights"][i],
                    "Area": f"{auc:.4f}",
                    "Concentration": "N/A",
                    "Units": "N/A"
                }
            )

        return row_data
    
    return no_update