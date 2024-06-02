import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from components.sidebar import sidebar
from components.graph import graph


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
)


app.layout = dmc.MantineProvider(
    html.Div(
        [
            sidebar,
            graph
        ],
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)
