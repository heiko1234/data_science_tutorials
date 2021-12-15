from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go


def plotly_distribution(data, target=None, online=False):
    """
    Plot the distributions of all variables next to one another

    Inputs:
        - data: data frame with variables to plot
        - target: means any parameter in the data, can be None
        - online False or True, False = plot
    """
    X_scaled = MinMaxScaler().fit_transform(data)

    if target is None:
        color = "royalblue"
    else:
        color = data[target]

    data_list = [go.Scatter(
                    x=i + 1 + 0.1*np.random.randn(data.shape[0]),
                    y=X_scaled[:, i],
                    mode='markers',
                    name=data.columns[i],
                    marker=dict(
                        size=10,
                        color=color
                    )
                ) for i in range(0, data.shape[1])]

    layout = {
        "xaxis": dict(
            range=(0, data.shape[1]+1),
            constrain="domain",
            ticktext=data.columns.to_list(),
            tickvals=list(range(1, data.shape[1]+1)),
        ),
        "yaxis": dict(
            range=(-0.05, 1.05),
            constrain="domain",
            title="scaled parameter",
        ),
        "title": dict(
            text="distribution of each parameter",
        ),
        "showlegend": False
    }

    fig = {
        "data": data_list,
        "layout": layout,
    }
    if online:
        return plotly.graph_objs.Figure(fig)
    else:
        plotly.offline.plot(fig, filename="plotly_data_distribution.html")

