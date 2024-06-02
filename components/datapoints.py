from dash import html
import dash_bootstrap_components as dbc


graph_datapoints = html.Div(
    [
        html.P("Set the number of datapoints:"),
        dbc.Input(type="number", placeholder="10-10000", value=1000, min=10, max=10000, step=1, id="graph-datapoints", className='sidebar-input')
    ]
)
