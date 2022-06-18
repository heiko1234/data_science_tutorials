
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.express as px



def paretoplot(data, column_of_names=None, column_of_values=None, yname=None, xname=None, title=None, plot=True):

    if column_of_names is None:
        column_of_names = list(data.columns)[0]
    if column_of_values is None:
        column_of_values = list(data.columns)[1]


    if xname is None:
        xname = column_of_names

    if yname is None:
        yname = "counts"

    data_sort = data.sort_values(by = column_of_values, ascending=False).reset_index(drop=True)

    Y_data = data_sort.loc[:, column_of_values].tolist()
    X_data = data_sort.loc[:, column_of_names].tolist()

    # x_list = [ "." + str(i) for i in X_data]
    x_list = [str(i) for i in X_data]
    x_list = np.asarray(x_list)

    y_per = [element_y / sum(Y_data) * 100 for element_y in Y_data]

    output = []
    for i in range(1, len(y_per)+1):
        output.append(sum(y_per[0:i]))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            name="Barplot",
            x = x_list,
            y = Y_data
        ),
        secondary_y = False
    )
    fig.add_trace(
        go.Scatter(
            x = x_list,
            y = output, 
            mode = "lines+markers",
            name = "percentage line", 
            marker = dict(
                color="red"
            )
        ),
        secondary_y = True
    )
    if title is None:
        title = "Paretoplot"
    fig.update_layout(
        title_text = title,
        xaxis = dict(categoryorder = "array", categoryarray = x_list)
    )
    fig.update_yaxes(
        title_text="percentage",
        range=(0, 101),
        showgrid= True,
        gridwidth=1,
        gridcolor="white", 
        secondary_y=True
        )
    fig.update_yaxes(
        title_text=yname,
        showgrid=True,
        gridwidth=1,
        gridcolor="black",
        secondary_y=False
        )
    fig.update_xaxes(
        title_text=xname,
        # showgrid=True,
        # gridwidth=1,
        # gridcolor="black",
        )

    if plot:
        plotly.offline.plot(fig, filename="paretoplot.html")
    else:
        return fig




def correlationplot(data, correlation_method=None, colorscale=None, title="Heatmap", hoferinfo=True, digits=3, annotation=False, plot=True):

    if correlation_method == None:
        correlation_method="pearson"

    corr = data.corr(method=correlation_method)
    corr=np.around(corr,digits)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    df_mask = corr.mask(mask)


    fig = None

    if colorscale==None:
        colorscale=px.colors.diverging.Picnic

    if hoferinfo == True: 
        hoferinfo = None
    else: 
        hoferinfo = "none"



    fig = ff.create_annotated_heatmap(
        z=df_mask.to_numpy(), 
        x=df_mask.columns.tolist(),
        y=df_mask.columns.tolist(),
        colorscale=colorscale,
        #colorscale=px.colors.sequential.Bluered,
        hoverinfo=hoferinfo, # "none", #Shows hoverinfo for null values
        showscale=True,
        ygap=1, 
        xgap=1,
        zmax=1, 
        zmin=-1
        )

    fig.update_xaxes(side="bottom")

    fig.update_layout(
        title_text=title, 
        title_x=0.5, 
        # width=1000, 
        # height=1000,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis_autorange='reversed',
        template='plotly_white'
    )

    # NaN values are not handled automatically and are displayed in the figure
    # So we need to get rid of the text manually
    if annotation: 
        for i in range(len(fig.layout.annotations)):
            if fig.layout.annotations[i].text == 'nan':
                fig.layout.annotations[i].text = ""
    else:
        for i in range(len(fig.layout.annotations)):
            fig.layout.annotations[i].text=""

    if plot:
        fig.show()
    else:
        return fig





