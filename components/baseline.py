from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH, no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


baseline_accordian = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Baseline",
                    icon=DashIconify(
                        icon="mdi:graph-bell-curve-cumulative",
                        color="black",
                        width=20,
                    ),
                ),
                dmc.AccordionPanel(
                    [
                        html.Div(
                            [
                                dmc.Switch(
                                    id="trendline-choice",
                                    color="red",
                                    onLabel=DashIconify(icon="covid:covid-carrier-blood-2"),
                                    offLabel=DashIconify(icon="codicon:graph-line"),
                                    size="xl",
                                    checked=False
                                ),
                            ],
                            id="baseline-switch",
                            style={"display": "flex", "justify-content": "center"}
                        ),
                        html.Hr(),
                        html.Div(id="baseline-container"),
                    ],
                    id="add-baseline-accordian"
                ),
            ],
            value="baseline-accordian",
        ),
    ]
)

bleed_options = dmc.Accordion(
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        f"Column Bleed",
                        icon=DashIconify(
                            icon="covid:covid-carrier-blood-2",
                            color="black",
                            width=20,
                        ),
                    ),
                    dmc.AccordionPanel(
                        [
                            html.Div(
                                [
                                    html.P("Bleed X Start:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=1000, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "bleed-start", "index": 1})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Bleed X Stop:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=1000, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "bleed-stop", "index": 1})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Bleed Height:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "bleed-height", "index": 1})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Slope Factor:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "bleed-slope", "index": 1})
                                ],
                                className="accordian-options"
                            ),
                        ],
                    ),
                ],
                value="bleed-accordian",
            ),
        ]
    )

trendline_choice = [
    html.Div(
        [
            dbc.Button("+ Add Trendline", id="add-trendline", style={"width": "100%"}),
            html.Hr()
        ],
        id="add-trendline-container"
    )
    
]

def trendline_options(n_clicks):
    return dmc.Accordion(
        children=[
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(f"Baseline Trend {n_clicks}", id={"type": "baseline-trendline", "index": n_clicks}),
                    dmc.AccordionPanel(
                        [
                            html.Div(
                                [
                                    html.P("Trendline X Start:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "baseline-start", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Trendline X Stop:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "baseline-stop", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    html.P("Slope Factor:", style={"margin-top": 10}),
                                    dbc.Input(type="number", value=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id={"type": "baseline-slope", "index": n_clicks})
                                ],
                                className="accordian-options"
                            ),
                            html.Div(
                                [
                                    dbc.Switch(label="Reset Baseline After?", id={"type": "reset_baseline", "index": n_clicks})
                                ],
                                className="accordian-options",
                                style={"margin-top": "1rem"}
                            ),
                        ],
                    ),
                ],
                value="baseline-accordian",
            ),
        ]
    )


@callback(
    Output("baseline-container", "children"),
    Input("trendline-choice", "checked"),
)
def switch_baseline_options(choice):
    if choice:
        return bleed_options
    return trendline_choice


@callback(
    Output("add-trendline-container", "children"),
    Input("add-trendline", "n_clicks"),
    prevent_initial_call=True
)
def add_trendline(n_clicks):
    patched_children = Patch()
    trendline = trendline_options(n_clicks)
    patched_children.append(trendline)
    return patched_children
    