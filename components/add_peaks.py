from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


peak_accordian = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Peaks",
                    icon=DashIconify(
                        icon="fa-brands:think-peaks",
                        color="black",
                        width=20,
                    ),
                ),
                dmc.AccordionPanel(
                    [
                        dbc.Button("+ Add Peak", id="add-peak"),
                        html.Hr()
                    ],
                    id="add-peak-accordian"
                ),
            ],
            value="peak-accordian",
        ),
    ]
)


def peak_options():
    return html.Div(
        [
            html.Div(
                [
                    html.P("Peak Center:", style={"margin-top": 10}),
                    dbc.Input(type="number", style={"width": 100, "margin-left": 20}, className="sidebar-input", id="peak-center")
                ],
                style={"display": "flex", "justify-content": "center", "align-items": "center"}
            ),
            html.Div(
                [
                    html.P("Peak Width:", style={"margin-top": 10}),
                    dbc.Input(type="number", style={"width": 100, "margin-left": 20}, className="sidebar-input", id="peak-width")
                ],
                style={"display": "flex", "justify-content": "center", "align-items": "center"}
            )
        ]
    )


@callback(
    Output("add-peak-accordian", "children"), Input("add-peak", "n_clicks"), prevent_initial_call=True
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    peak = peak_options()
    patched_children.append(peak)
    return patched_children
