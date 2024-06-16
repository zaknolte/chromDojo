from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np

integration_accordian = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Integration Parameters",
                    icon=DashIconify(
                        icon="tabler:math-integral-x",
                        color="black",
                        width=20,
                    ),
                ),
                dmc.AccordionPanel(
                    [
                        html.Div(
                            [
                                html.P("Enable Autointegration:"),
                                dmc.Switch(
                                    id="auto-integration",
                                    color="green",
                                    onLabel=DashIconify(icon="quill:off"),
                                    offLabel=DashIconify(icon="quill:off"),
                                    size="xl",
                                    checked=False
                                ),
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Peak Width:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-width")
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Peak Height:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-height")
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Threshold:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-threshold")
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Distance:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=1, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-distance")
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Prominence:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=10, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-prominence")
                            ],
                            className="accordian-options"
                        ),
                        html.Div(
                            [
                                html.P("Integration Width:", style={"margin-top": 10}),
                                dbc.Input(type="number", value=50, min=5, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="integration-wlen")
                            ],
                            className="accordian-options"
                        ),
                    ]
                ),
            ],
            value="integration-accordian",
        ),
    ]
)