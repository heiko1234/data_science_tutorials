
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE

import plotly
import plotly.graph_objs as go


def _plot(x, y, color="royalblue", plot=True):
    """A fix scatter plot

    Args:
        x (_type_): _description_
        y (_type_): _description_
        color (str, optional): _description_. Defaults to "royalblue".
        plot (bool, optional): _description_. Defaults to True.
    """

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            mode="markers", 
            x = x,
            y = y, 
            marker = dict(
                color = color
            )
        )
    )
    try: 
        title = str(y.name) + " vs. " + str(x.name)
        fig.update_layout(
            title_text = title
        )
    except BaseException:
        pass
    if plot:
        plotly.offline.plot(fig, filename="fixplot.html")
    else:
        return fig


def make_TSNE_plot(features, target, plot=True):
    """make a TSNE plot

    Args:
        features (_type_): _description_
        target (_type_): _description_
        plot (bool, optional): _description_. Defaults to True. True give plot, else a dic.

    Returns:
        _type_: _description_
    """

    if isinstance(features, np.ndarray):
        features_np = features
    elif isinstance(features, pd.DataFrame):
        features_np = features.to_numpy()
    if isinstance(target, pd.DataFrame):
        target_df = target
    elif isinstance(target, np.ndarray):
        target_df = pd.DataFrame(data = target, columns = ["target"])
    elif isinstance(target, pd.Series):
        target_df = target.to_frame()
    
    
    tsne_features = TSNE(n_components=2).fit_transform(features_np)

    tsne_features_df = pd.DataFrame(data=tsne_features, columns = ["x", "y"])

    output_df = pd.concat([tsne_features_df, target_df], axis = 1)

    if plot:
        _plot(y=output_df.loc[:, "y"], x=output_df.loc[:, "x"], color=output_df.iloc[:,2], plot=True)
    else:
        return output_df



