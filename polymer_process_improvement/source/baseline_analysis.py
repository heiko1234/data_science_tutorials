

import pandas as pd
import numpy as np
import plotly.express as px

from polymer_process_improvement.source.control_chart import simple_controlchart
from polymer_process_improvement.source.nelson_controlchart import control_chart


data = pd.read_csv("/home/heiko/Repos/data_science_tutorials/polymer_process_improvement/data/BaselineYieldData.csv", sep=",")

data.head()


# ups, this does not work
fig = px.scatter(x=data["Date"], y=data["Yield / %"])
fig.show()


data.columns
data.dtypes


data["date"] = pd.to_datetime(data["Date"], format="%d.%m.%y")

data.head()
data.columns
data.dtypes



data["Yield"] = data["Yield / %"].str.replace(",", ".")

data["Yield"] = pd.to_numeric(data["Yield"], errors='coerce')


fig = px.scatter(x=data.iloc[:,2], y=data.iloc[:,3])
fig.show()


# set a filter, only values above 85.0 % yield
fdata = data[data["Yield"] >= 85.0]

fig = px.scatter(x=fdata.iloc[:,2], y=fdata.iloc[:,3])
fig.show()


# not filtered 
np.average(data["Yield"])   #88.2

# filtered
np.average(fdata["Yield"])  #94.0


data.columns
control_chart(data =data, y_name="Yield", xlabel = None, title = "Controlchart Yield", lsl = 85, usl = None, outlier = False, lines= False, mean = None, sigma = None)

simple_controlchart(data =data, y_name="Yield", title = "Controlchart Yield", target=None, xlabel=None, Phase=None, Phasesinplot= True, Outlier = False, plotlimit=False)





