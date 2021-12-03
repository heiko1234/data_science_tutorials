

# https://www.pybloggers.com/2016/03/three-ways-to-do-a-two-way-anova-with-python/

# https://sixsigmastudyguide.com/repeatability-and-reproducibility-rr/


import pandas as pd
import numpy as np


import statsmodels.api as sm
from statsmodels.formula.api import ols

import plotly.express as px




def plot_on_groups(data, x=part, y=result, color =operator, analysis = "mean"):
    
    if analysis == "mean":
        data_mean = data.groupby([x, color]).mean()
    if analysis == "std":
        data_mean = data.groupby([x, color]).std()
    if analysis == "var":
        data_mean = data.groupby([x, color]).var()
    data_mean = data_mean.reset_index()
    fig = px.line(data_mean, x = x, y = y, color = color, markers=True)
    fig.show()


def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['mse_sq']/sum(aov['sum_sq'])
    return aov


def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov


def mean_squared(aov): 
    aov["mse_sq"] = aov["sum_sq"]/aov["df"]
    return aov


def ratio_aov(aov, total_of="sum_sq"):
    sum = np.sum(aov[total_of])
    name = "ratio_"+total_of
    aov[name] = aov[total_of]/sum*100
    return aov


def dict_av_group(data, group, result):
    output = {}
    for element in set(data[group]):
        output[element] = np.average(data[data[group]==element][result])
    return output


def sigma_interaction(anova_table, operator, instument,  part, num_parts, num_instruments):
    if instument == None:
        sigma_interaction = (anova_table.loc[f"C({operator}):C({part})","mse_sq"] - anova_table.loc[f"Residual","mse_sq"] ) / num_parts
    else: 
        sigma_interaction = (anova_table.loc[f"C({operator}):C({part})","mse_sq"] + anova_table.loc[f"C({operator}):C({instrument})","mse_sq"]  - anova_table.loc[f"Residual","mse_sq"]/(num_instruments) ) / num_parts
    sigma_interaction
    if sigma_interaction < 0:
        sigma_interaction = 0
    return sigma_interaction


def mean_dict_to_average(dict, mean):
    output = []
    for key in dict:
        output.append((dict[key] - mean)**2)
    return(output)


def gagernr(data, operator=None, instrument = None, part= None, result=None):

    # repeatability, same part by same operator by same instrument

    # reporducibility, same part, different operators, different instrument

    if instrument != None:
        model = ols(f'{result} ~ C({part}) + C({operator}) + C({instrument}) + C({part}):C({instrument}) + C({operator}):C({instrument}) + C({operator}):C({part})', data=data).fit()
    
    if instrument == None:
        model = ols(f'{result} ~ C({part}) + C({operator}) + C({operator}):C({part})', data=data).fit()


    # OLS regression
    # print(model.summary()) # print F-stat, eta², P value but also test indicators for assumptions


    anova_table = sm.stats.anova_lm(model, typ='II') 
    anova_table

    mean_squared(anova_table)
    ratio_aov(anova_table, total_of="sum_sq")


    # we then prepare a multiple comparison set:
    #mult_comp = sm.stats.multicomp.MultiComparison(data['MFI'], data['Instrument']) 
    # Tukey post-hoc testing, for example
    #print(mult_comp.tukeyhsd()) 

    #dict_av_group(data=data, group= operator, result=result)
    #dict_av_group(data=data, group= part, result=result)
    #if instrument != None:
    #    dict_av_group(data=data, group= instrument, result=result)


    av = np.average(data[result])
    av  # 197.834


    num_parts = len(set(data[part])) 
    num_operator = len(set(data[operator]))

    if instrument != None:
        num_instruments = len(set(data[instrument]))
    else: 
        num_instruments=1
    num_repeats = len(data)/(num_instruments*num_operator*num_parts)

    num_parts
    num_operator
    num_instruments
    num_repeats

    #np.sum([(v-av)**2 for v in data[result]])
    #np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= operator, result=result), mean= av))
    #np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= instrument, result=result), mean= av))
    #np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= part, result=result), mean= av))

    #ss_operator =  np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= operator, result=result), mean= av))
    #ss_instrument =  np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= instrument, result=result), mean= av))
    #ss_part= np.sum(mean_dict_to_average(dict=dict_av_group(data=data, group= part, result=result), mean= av))
    #ss_total = np.sum([(v-av)**2 for v in data[result]])

    anova_table


    if instrument == None: 
        sigma_operator = (anova_table.loc[f"C({operator})","mse_sq"] - anova_table.loc[f"C({operator}):C({part})","mse_sq"] ) / (num_parts * num_repeats)
    else: 
        sigma_operator = (anova_table.loc[f"C({operator})","mse_sq"] - anova_table.loc[f"C({operator}):C({part})","mse_sq"] - anova_table.loc[f"C({operator}):C({instrument})","mse_sq"]  ) / num_parts * num_repeats #*num_instruments)
    sigma_operator= abs(sigma_operator)  #0.09911


    sigma_interactions = abs(sigma_interaction(anova_table, operator, instrument, part, num_parts, num_instruments))
    sigma_interactions

    sigma_reproducable = sigma_operator+sigma_interactions
    sigma_reproducable


    sigma_repeatability = anova_table.loc[f"Residual","mse_sq"] 
    sigma_repeatability

    gagernr = sigma_repeatability + sigma_reproducable
    gagernr 
    
    if instrument == None: 
        part_to_part = (anova_table.loc[f"C({part})","mse_sq"] - anova_table.loc[f"C({operator}):C({part})","mse_sq"] ) / (num_operator*num_repeats)
    else: 
        part_to_part = (anova_table.loc[f"C({part})","mse_sq"] - anova_table.loc[f"C({operator}):C({part})","mse_sq"] - anova_table.loc[f"C({operator}):C({instrument})","mse_sq"] ) / (num_operator*num_repeats*num_instruments)
    part_to_part 

    sigma_total = gagernr + part_to_part + sigma_interactions
    sigma_total


    new_rows= ["Gage R&R", "Repeatability", "Reproducibility", "Interaction Variation", "part-to-part Variation", "Total Variation"]


    df = pd.DataFrame()
    df["names"] = new_rows
    df["variations"] = [gagernr, sigma_repeatability, sigma_reproducable,  sigma_interactions, part_to_part, sigma_total]
    #df["percent of total"] = np.sqrt(df["variations"])/np.sqrt(sigma_total)*100
    df["percent of total"] = round(df["variations"]/sigma_total*100, 3)

    # update percentags
    df

    df.loc[1, "percent of total"] = round(df.loc[1, "variations"] / df.loc[0, "variations"] *df.loc[0, "percent of total"],3)
    df.loc[2, "percent of total"] = round(df.loc[2, "variations"] / df.loc[0, "variations"] *df.loc[0, "percent of total"],3)


    #df["percent of total"] = df["variations"]/sigma_total*100
    df

    return df



#########

data = pd.read_csv("./polymer_process_improvement/data/MSA_MFI_Final.csv")
data

# data = data.iloc[:,2:]
data 


operator = "Operator"
instrument = "Instrument"
part = "Batch"
result = "MFI"


##########

data = pd.read_csv("./polymer_process_improvement/data/MSA_Xf_Final.csv")
data

#data = data.iloc[:,1:]
data 


operator = "Operator"
instrument = "Instrument"
part = "Batch"
result = "Xf"




plot_on_groups(data = data, x = part, y = result, color=operator, analysis = "mean")
plot_on_groups(data = data, x = part, y = result, color=instrument, analysis = "mean")

plot_on_groups(data = data, x = part, y = result, color=operator, analysis = "std")
plot_on_groups(data = data, x = part, y = result, color=instrument, analysis = "std")




gagernr(data=data, operator=operator, instrument = instrument, part= part, result=result)


group = part
dict_av_group(data, group=group, result=result)

np.average(mean_dict_to_average(dict=dict_av_group(data=data, group= group, result=result), mean= np.average(data[result])))


