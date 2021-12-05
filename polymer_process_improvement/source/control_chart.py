

import plotly.graph_objects as go
import pandas as pd
import numpy as np



def make_Phasis_dict(data, Phases=None):
    output = {}
    if Phases is not None:
        keys = list(set(data[Phases]))

        for element in keys:
            output[element] = [min(data[data[Phases]==element].index), max(data[data[Phases]==element].index)]
    else: 
        output["all"] = [min(data.index), max(data.index)]

    return output



def make_data_dict(data, y_name, Phases=None):
    data_dict = {}
    if Phases is not None:
        for key in Phases:
            data_av = np.average(data.loc[Phases[key][0]:Phases[key][1], y_name])
            data_std = np.std(data.loc[Phases[key][0]:Phases[key][1], y_name])
            data_dict[key] = [data_av, data_std]
    else: 
        data_dict["all"] = [np.average(data[y_name]), np.std(data[y_name])]
    return data_dict



def get_outofrange(data, y_name, data_dict, Phasis_dict):
    output = []
    for keys in data_dict.keys():

        if list(data_dict.keys()) != 1:

            av = data_dict[keys][0]
            sd = data_dict[keys][1]
            index_start=Phasis_dict[keys][0]
            index_ende=Phasis_dict[keys][1]

            output.append((data.loc[index_start:index_ende, y_name] >= av+3*sd) | (data.loc[index_start:index_ende, y_name] <= av-3*sd) )

    output = pd.concat(output)
    output = output.sort_index()
    return output



def simple_controlchart(data, y_name, title = None, target=None, xlabel=None, Phase=None, Phasesinplot= True, Outlier = True, plotlimit=True):

    if Phase is not None: 
        # Indexes of Phases starts or ends
        Phasis_dict = make_Phasis_dict(data=data, Phases=Phase)
        # for each phase, average and std
        data_dict = make_data_dict(data=data, y_name=y_name, Phases=Phasis_dict)
        # outlier indexes
        output  = get_outofrange(data=data, y_name=y_name, data_dict=data_dict, Phasis_dict=Phasis_dict)
    
    if Phase is None:
        Phasis_dict = make_Phasis_dict(data=data, Phases=None)
        data_dict = make_data_dict(data=data, y_name=y_name, Phases=None)
        output  = get_outofrange(data=data, y_name=y_name, data_dict=data_dict, Phasis_dict=Phasis_dict)
        #av = np.average(data[y_name])
        #std = np.std(data[y_name])

        #output = (data.loc[:, y_name] >= av+3*std) | (data.loc[:, y_name] <= av-3*std)

    if xlabel is not None: 
        if isinstance(data[xlabel], pd.Series):
            label_list = data[xlabel].tolist()
            label_list = [str(i) for i in label_list]
            label_val = list(data.index)
        else:
            label_list = None
            label_val = None


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data[y_name], mode='markers', name=y_name))

    if plotlimit:
        for element in data_dict.keys():

            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0],
                    line=dict(
                        color='black',
                    )
                )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]+data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]+data_dict[element][1],
                    line=dict(
                        color='grey',
                    )
                )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]-data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]-data_dict[element][1],
                    line=dict(
                        color='grey',
                    )
            )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]+2*data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]+2*data_dict[element][1],
                    line=dict(
                        color='grey',
                    )
                )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]-2*data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]-2*data_dict[element][1],
                    line=dict(
                        color='grey',
                    )
            )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]+3*data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]+3*data_dict[element][1],
                    line=dict(
                        color='red',
                    )
                )
            fig.add_shape(type='line',
                    x0=Phasis_dict[element][0],
                    y0=data_dict[element][0]-3*data_dict[element][1],
                    x1=Phasis_dict[element][1],
                    y1=data_dict[element][0]-3*data_dict[element][1],
                    line=dict(
                        color='red',
                    )
                )

    if Outlier:

        fig.add_trace(go.Scatter(x=data.loc[output, y_name].index, y=data.loc[output, y_name], mode='markers', name="Outliers", marker=dict(
                color="red") ))

    if Phasesinplot:

        for element in Phasis_dict.keys():

            xpos = round((Phasis_dict[element][0])/max(data.index),2)+round((Phasis_dict[element][1]-Phasis_dict[element][0])/(2*max(data.index)),2)

            if element != "all":
                fig.add_annotation(text=element,
                                xref="paper", yref="paper",
                                x=xpos, y=0.05, showarrow=False)
    
    if target is not None:
        fig.add_shape(type='line',
                    x0=min(data.index),
                    y0=target,
                    x1=max(data.index),
                    y1=target,
                    line=dict(
                        color='blue',
                    )
                )


    if xlabel is not None:
        fig.update_xaxes(
                ticktext = label_list,
                tickvals = label_val
                )

    fig.update_layout(
        title=title)

    fig.show()


