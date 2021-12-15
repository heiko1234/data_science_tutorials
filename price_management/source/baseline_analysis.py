
# baseline_analysis.py

# imports

import plotly.express as px

import pandas as pd

# 
from sklearn.preprocessing import MinMaxScaler
import plotly
import plotly.graph_objs as go
import numpy as np

# Load the data

data = pd.read_csv("./price_management/data/baseline.csv")


def translate(data, columnlist):
    for element in columnlist:
        try:
            data[element] = data[element].str.replace(",", ".")
            data[element] = pd.to_numeric(data[element], errors='coerce')
        except:
            continue
    return data


data = translate(data = data, columnlist = ["Price Increase"])


data
data.columns


fig = px.bar(data, x = "Product Category")
fig.show()



# or as for loop

for element in data.columns:
    fig = px.bar(data, x = element)
    fig.show()


data.columns

# ['Product Code', 'Region', 'Customer ID', 'Supply Demand Balance',
# 'Sales Rep', 'Sales Rep Experience', 'Buyer Sophistication',
# 'Product Category', 'Annual Volume Purchased', 'Price Increase',
# 'Defective'],



fig = px.bar(data, x = "Supply Demand Balance", color= "Defective")
fig.show()



data_crosstab = pd.crosstab(data["Supply Demand Balance"],data["Defective"], margins = False)
data_crosstab

data_crosstab = pd.crosstab(data["Supply Demand Balance"],data["Defective"], margins = True)
data_crosstab

data_crosstab = pd.crosstab(data["Supply Demand Balance"],data["Defective"], margins = True, normalize="index")
data_crosstab

data_crosstab = pd.crosstab(data["Supply Demand Balance"],data["Defective"], margins = True, normalize=True)
data_crosstab

data_crosstab = pd.crosstab(data["Supply Demand Balance"],data["Defective"], margins = True, normalize="index")
data_crosstab


fig =  px.histogram(data, x="Price Increase", nbins=20, marginal="box")
fig.show()


fig =  px.histogram(data, x="Price Increase", color = "Supply Demand Balance", nbins=20, marginal="box")
fig.show()




# or as for loop

for element in data.columns:
    fig = px.histogram(data, x = element, color = "Defective" )
    fig.show()





data

target = "Price Increase"
column = "Supply Demand Balance"

np.average(data[target])
color="royalblue"

len(list(set(data[column])))


def oneway_plot(data, target, column, color="royalblue"):


    fig = go.Figure()

    habline = np.average(data[target])
    fig.add_hline(y=habline)

    for  count, value in enumerate(list(set(data[column]))):

        idata = data[data[column]== value].reset_index(drop = True)

        fig.add_trace(go.Scatter(
            x= count + 1 + 0.1*np.random.randn(idata.shape[0]),
            y = idata[target],
            name=value,
            mode='markers',
            marker=dict(
                        size=10,
                        color=color
                    )
        )) 


    plotly.offline.plot(fig, filename="plotly_data_distribution.html")



oneway_plot(data=data, target="Price Increase", column="Supply Demand Balance")
oneway_plot(data=data, target="Price Increase", column="Buyer Sophistication")
oneway_plot(data=data, target="Price Increase", column="Product Category")



my_plot_list = ["Product Category","Supply Demand Balance","Buyer Sophistication" ]



for i in my_plot_list: 
    fig = px.box(data, y="Price Increase", x =i, points="all")
    fig.show()


for i in my_plot_list: 
    fig = px.box(data, y="Price Increase", x =i, points="all", color="Defective")
    fig.show()





