import plotly.graph_objects as go
import numpy as np
import peakutils

x = np.linspace(0, 120, 121)
noise = np.random.rand(x.size) * 10
y = (peakutils.gaussian(x, 50, 10, 3) +
     peakutils.gaussian(x, 251, 71, 5) +
     peakutils.gaussian(x, 81, 85, 2) +
     noise)


fig = go.Figure(
    go.Scatter(
        x=x,
        y=y
    ),
    layout={
        'paper_bgcolor': 'rgba(0,0,0,0)',
    },
)
