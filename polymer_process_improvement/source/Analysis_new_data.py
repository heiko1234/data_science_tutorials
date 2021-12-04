


import pandas as pd
import numpy as np


import statsmodels.api as sm
from statsmodels.formula.api import ols

import plotly.express as px



data = pd.read_csv("./polymer_process_improvement/data/VSSTamData.csv")

data


# apply a filter for values smaller 85 %
data["select"] = 0

#
data.loc[data["Yield"] <= 85.0, "select"] = 1

#
(data["MFI"] < 192) | (data["CI"] < 80)

#
data.loc[data["MFI"] < 192, "select"] = 1
data.loc[data["CI"] < 80, "select"] = 1
data

data[data["select"]==1].count()  #28
data[data["select"]==0].count()  #82


fig = px.histogram(data, x="Yield", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


fig = px.histogram(data, x="MFI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


fig = px.histogram(data, x="CI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


data.columns
fig = px.scatter(data, x = "Batch Number", y = "CI", )
fig.show()



data["yield_selection"]= 0
data.loc[data["Yield"] < 60, "yield_selection"] = 1

fig = px.scatter(data, x = "MFI", y = "Yield", color = "yield_selection")
fig.show()

fig = px.scatter(data, x = "CI", y = "Yield", color = "yield_selection")
fig.show()


fig = px.scatter(data, x = "Xf", y = "CI", color = "yield_selection")
fig.show()









