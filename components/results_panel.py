from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import peakutils
from scipy.signal import find_peaks
import jsonpickle

results_panel = dmc.TabsPanel(
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
                "icons": {
                    "sortAscending": '<i class="fa fa-solid fa-pencil">',
                    "sortDescending": '<i class="fa fa-solid fa-pencil"/>',
                },
                "sort": "desc",
                "editable": True
                # "sortable": False
            },
        ],
        dashGridOptions={
            "animateRows": True,
            },
        style={"width": None, "height": 500},
        className="ag-theme-balham-dark"
    ),
    value="results"
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
            if peak.area == 0:
                conc = 0
            else:
                conc = peak.calibration.calculate_concentration(peak.area)
            row_data.append(
                {
                    "RT": f"{peak.center:.2f} min",
                    "Name": peak.name,
                    "Height": f"{peak.height:.2f}",
                    "Area": f"{peak.area:.2f}",
                    "Concentration": f"{conc:.2f}",
                    "Units": peak.calibration.units
                }
            )

        return row_data
    
    return no_update

@callback(
    Output("x-y-data", "data", allow_duplicate=True),
    Input("results-table", "cellValueChanged"),
    State("x-y-data", "data"),
    prevent_initial_call=True
)
def update_units(units, graph_data):
    peaks = jsonpickle.decode(graph_data["peaks"])
    for peak in peaks:
        if peak.name == units[0]["data"]["Name"]:
            peak.calibration.units = units[0]["data"]["Units"]
    return {"x": graph_data["x"], "y": graph_data["y"], "peaks": jsonpickle.encode(peaks)}
