

import pandas as pd
import numpy as np
import plotly.express as px



data = pd.read_csv("./polymer_process_improvement/data/CrisisTeamData.csv", sep=",")

data.head()

data.dtypes

dict_Quarry={"Umbogo A": "Sup 1", "Kuanga A": "Sup 2", "Kuanga B": "Sup 3"}

data["Quarry"] = data["Quarry"].replace(dict_Quarry)


data.head()





def translate(data, columnlist):
    for element in columnlist:
        try:
            data[element] = data[element].str.replace(",", ".")
            data[element] = pd.to_numeric(data[element], errors='coerce')
        except:
            continue
    return data

data
data = translate(data = data, columnlist= ["Batch Nummer", "MFI", "CI", "Yield", "SA", "M%", "Xf", "pH", "Viscosity", "Ambient Temp"])

data

# data.to_csv("./polymer_process_improvement/data/CrisisTeamData.csv")



data.rename(columns={'Ambient Temp':'Temp'}, inplace=True)

data.rename(columns={'Batch Nummer':'Batch_number'}, inplace=True)

data


data.to_csv("./polymer_process_improvement/data/CrisisTeamData.csv")




