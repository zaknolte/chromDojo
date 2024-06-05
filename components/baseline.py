from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback, MATCH
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
                        dmc.Accordion(
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
                                                        dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="bleed-start")
                                                    ],
                                                    className="accordian-options"
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("Bleed X Stop:", style={"margin-top": 10}),
                                                        dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="bleed-stop")
                                                    ],
                                                    className="accordian-options"
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("Bleed Height:", style={"margin-top": 10}),
                                                        dbc.Input(type="number", value=0, min=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="bleed-height")
                                                    ],
                                                    className="accordian-options"
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("Slope Factor:", style={"margin-top": 10}),
                                                        dbc.Input(type="number", value=0, style={"width": 100, "margin-left": 20}, className="sidebar-input", id="bleed-slope")
                                                    ],
                                                    className="accordian-options"
                                                ),
                                            ],
                                        ),
                                    ],
                                    value="bleed-accordian",
                                ),
                            ]
                        ),
                        dbc.Button("+ Add Trendline", id="add-trendline", style={"width": "100%"}),
                        html.Hr()
                    ],
                    id="add-baseline-accordian"
                ),
            ],
            value="baseline-accordian",
        ),
    ]
)


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
    Output("add-baseline-accordian", "children"),
    Input("add-trendline", "n_clicks"),
    prevent_initial_call=True
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    trendline = trendline_options(n_clicks)
    patched_children.append(trendline)
    return patched_children
