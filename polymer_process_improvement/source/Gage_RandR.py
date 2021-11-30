

import pandas as pd
import numpy as np

from GaugeRnR import GaugeRnR

import plotly.express as px


# data = n[i, j, k]
# i = operator, j = part, k = measurement

data = pd.read_csv("./polymer_process_improvement/data/MSA_MFI_initial.csv")
data

data = data.iloc[:,2:]
data 



def plot_on_groups(data, x="Batch", y="MFI", color ="Technician", analysis = "mean"):
    
    if analysis == "mean":
        data_mean = data.groupby([x, color]).mean()
    if analysis == "std":
        data_mean = data.groupby([x, color]).std()
    data_mean = data_mean.reset_index()
    fig = px.line(data_mean, x = x, y = y, color = color, markers=True)
    fig.show()



plot_on_groups(data = data, x = "Batch", y = "MFI", color="Technician", analysis = "mean")
plot_on_groups(data = data, x = "Batch", y = "MFI", color="Instrument", analysis = "mean")

plot_on_groups(data = data, x = "Batch", y = "MFI", color="Technician", analysis = "std")
plot_on_groups(data = data, x = "Batch", y = "MFI", color="Instrument", analysis = "std")





data_np = data.to_numpy()
data_np



g = GaugeRnR(data_np)
g.calculate()

print(g.summary())
