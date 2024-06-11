from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# base peak accordion - no peaks exist by default
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
                        dbc.Button("+ Add Peak", id="add-peak", style={"width": "100%"}),
                        html.Hr()
                    ],
                    id="add-peak-accordian"
                ),
            ],
            value="peak-accordian",
        ),
    ]
)

# new peak accordion with all peak editing options
def peak_options(n_clicks):
    return dmc.Accordion(
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(f"Peak {n_clicks}", id={"type": "peak-set-name", "index": n_clicks}),
                    dmc.AccordionPanel(
                        [
                            html.Div(
                                [
                                    dbc.Input(placeholder=f"Peak {n_clicks}", type="text", id={"type": "peak-edit-name", "index": n_clicks}),
                                    dbc.Button(DashIconify(icon="ph:pencil-thin"), disabled=True)
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    dbc.Switch(label="Add label annotation", id={"type": "peak-add-annotation", "index": n_clicks})
                                ],
                                className="accordian-options",
                                style={"margin-top": "1rem"}
                            ),
                            html.Div(
                                [
                                    html.P("Peak Center:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "peak-center", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Peak Height:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "peak-height", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Peak Width:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "peak-width", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Skew Factor:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, step=0.1, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "peak-skew", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                        ],
                    ),
                ],
                value="peak-accordian",
            ),
        ]
    )

# Add another peak accordian with all peak options
@callback(
    Output("add-peak-accordian", "children"), Input("add-peak", "n_clicks"), prevent_initial_call=True
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    peak = peak_options(n_clicks)
    patched_children.append(peak)
    return patched_children

# Rename peak
@callback(
    Output({'type': 'peak-set-name', 'index': MATCH}, "children"),
    Input({'type': 'peak-edit-name', 'index': MATCH}, "value"),
    prevent_initial_call=True
)
def set_peak_name(name):
    return name
