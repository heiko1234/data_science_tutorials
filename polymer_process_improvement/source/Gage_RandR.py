

# https://www.pybloggers.com/2016/03/three-ways-to-do-a-two-way-anova-with-python/

import pandas as pd
import numpy as np


import statsmodels.api as sm
from statsmodels.formula.api import ols

import plotly.express as px




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


data.columns



model = ols('MFI ~ C(Batch) + C(Technician) + C(Instrument) + C(Batch):C(Instrument) + C(Technician):C(Instrument) + C(Batch):C(Instrument)', data=data).fit() # OLS regression
#print(model.summary()) # print F-stat, eta², P value but also test indicators for assumptions

anova_table = sm.stats.anova_lm(model, typ='II') # here we prepare a proper ANOVA table
print(anova_table)


def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    return aov


def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov


eta_squared(anova_table)
omega_squared(anova_table)
print(anova_table)


# we then prepare a multiple comparison set:
mult_comp = sm.stats.multicomp.MultiComparison(data['MFI'], data['Instrument']) 
print(mult_comp.tukeyhsd()) # Tukey post-hoc testing, for example












