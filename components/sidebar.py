from dash import html
import dash_bootstrap_components as dbc

from components.graph import graph_datapoints
from components.add_peaks import peak_accordian
from components.noise import noise_accordian


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
                noise_accordian
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)