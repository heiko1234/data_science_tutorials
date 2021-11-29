

import pandas as pd
import numpy as np
import plotly.express as px



data = pd.read_csv("./polymer_process_improvement/data/CrisisTeamData.csv", sep=",")

data.head()

data = data.iloc[:,1:]

data["select"] = 1

data.loc[data["Yield"] <= 85.0, "select"] = 0

data


fig = px.histogram(data, x="Yield", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()

fig = px.histogram(data, x="MFI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()

fig = px.histogram(data, x="CI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


