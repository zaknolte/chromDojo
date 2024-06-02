from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


noise_accordian = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Noise",
                    icon=DashIconify(
                        icon="icon-park-outline:electric-wave",
                        color="black",
                        width=20,
                    ),
                ),
                dmc.AccordionPanel(
                    html.Div(
                        [
                            html.P("Add Noise:", style={"margin-top": 10}),
                            dbc.Input(type="number", style={"width": 100, "margin-left": 20}, className="sidebar-input", id="add-noise")
                        ],
                        style={"display": "flex", "justify-content": "center", "align-items": "center"}
                    ),
                ),
            ],
            value="noise-accordian",
        ),
    ]
)
