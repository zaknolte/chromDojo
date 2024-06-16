from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

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
                dmc.TabsPanel("results data here", value="results"),
                dmc.TabsPanel("curve data here", value="curves"),
            ],
            value="results",
            color="red",
            style={"width": "60%"}
        ),
    ],
    style={"display": "flex", "justifyContent": "center"}
)