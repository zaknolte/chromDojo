from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np
import peakutils
from scipy.signal import find_peaks
import jsonpickle

from components.results_panel import results_panel
from components.calibration_panel import calibration_panel

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
                results_panel,
                calibration_panel
            ],
            value="results",
            color="red",
            style={"width": "60%"}
        ),
    ],
    style={"display": "flex", "justifyContent": "center"}
)
