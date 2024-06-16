from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import numpy as np

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
                            html.P("Noise Factor:", style={"margin-top": 10}),
                            dbc.Input(type="number", value=0, placeholder=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="add-noise")
                        ],
                        style={"display": "flex", "justify-content": "center", "align-items": "center"}
                    ),
                ),
            ],
            value="noise-accordian",
        ),
        dcc.Store(id="noise-data")
    ]
)


# noise needs to be calculated and stored separately to keep it 'static' until explicitly changed
# otherwise it gets recalculated on every single update to fig resulting in bad UX
@callback(
    Output("noise-data", "data"),
    Input("graph-datapoints", "value"),
    Input("add-noise", "value"),
)
def update_noise(datapoints, noise_factor):
    x = np.linspace(0, datapoints, datapoints + 1)
    return np.random.rand(x.size) * noise_factor