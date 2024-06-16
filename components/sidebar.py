from dash import html
import dash_bootstrap_components as dbc

from components.datapoints import graph_datapoints
from components.add_peaks import peak_accordian
from components.noise import noise_accordian
from components.baseline import baseline_accordian
from components.annotations import annotations_accordian
from components.integration import integration_accordian


sidebar = html.Div(
    [
        html.Div(
            [html.I(className="fa-solid fa-sliders me-2"),
             html.Span("Options")],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                graph_datapoints,
                html.Hr(),
                peak_accordian,
                html.Hr(),
                noise_accordian,
                html.Hr(),
                baseline_accordian,
                html.Hr(),
                annotations_accordian,
                html.Hr(),
                integration_accordian
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)
