import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from components.graph import fig

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
)


sidebar = html.Div(
    [
        html.Div(
            [html.I(className="fa-solid fa-sliders me-2"),
             html.Span("Settings")],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                html.H2("test 1"),
                html.H5("test 2")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

app.layout = html.Div(
    [
        sidebar,
        dcc.Graph(figure=fig, className='content')
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
