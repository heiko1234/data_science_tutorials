

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly

import statistics

import pandas as pd





def multi_vari_plot(data, operator, part, parameter, plot=True):

    operators = list(set(data[operator]))
    number_of_operators = len(operators)

    fig = make_subplots(
        cols = number_of_operators, 
        rows= 1, 
        shared_yaxes=True,
        horizontal_spacing=0.01
        )
    fig.update_yaxes(title_text=parameter, row=1, col=1)

    overall_mean = round(statistics.mean(data[parameter]),3)

    for count, value in enumerate(operators):

        df = data[data[operator]==value]
        df = df.sort_values(by=part)
        try:
            df[part] = df[part].astype(str)
        except BaseException:
            pass
        df = df.reset_index(drop = True)
        subset_mean = round(statistics.mean(df[parameter]),3)
        fig.append_trace(
            go.Scatter(
                x=df[part],
                y=df[parameter],
                mode="markers",
                marker=dict(
                    size=12
                ),
                name=value
            ),
            col = count+1, 
            row = 1
        )
        fig.update_xaxes(title_text=value, col=count+1, row=1)
        fig.add_hline(y=subset_mean, 
            row=1, col=count+1,
            annotation_text=f"mean:{subset_mean}", 
            annotation_position="bottom right")

        fig.add_hline(y=overall_mean, line_dash="dot")

    fig.add_hline(y=overall_mean, line_dash="dot",
        annotation_text=f"avg:{overall_mean}",
        annotation_position="top right",
        col=number_of_operators,
        row=1)

    if plot:
        return plotly.offline.plot(fig)

    else:
        return fig


def make_muti_vari_plot(data, operator, part, parameter, type=None, plot=True):

    if type=="std" or type=="STD":
        data = data.groupby([part, operator]).std(numeric_only=True)
        data = data.reset_index(drop = False)

    elif type=="mean" or type == "average":
            data = data.groupby([part, operator]).mean(numeric_only=True)
            data = data.reset_index(drop = False)

    output = multi_vari_plot(
        data=data,
        operator=operator,
        part=part,
        parameter=parameter,
        plot=plot
        )
    return output



