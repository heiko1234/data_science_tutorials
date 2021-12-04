
import pandas as pd
import numpy as np


data = pd.read_csv("./polymer_process_improvement/data/MSA_MFI_initial.csv")


data = pd.read_csv("./polymer_process_improvement/data/VSSTamData.csv")



data



dict_technicans={"Janet": "Klaus", "Frank":"Peter", "Bob": "Hans"}


data["Operator"] = data["Operator"].replace(dict_technicans)

data.rename(columns={"Operator":"Technician"}, inplace = True)


def translate(data, columnlist):
    for element in columnlist:
        try:
            data[element] = data[element].str.replace(",", ".")
            data[element] = pd.to_numeric(data[element], errors='coerce')
        except:
            continue
    return data


data = translate(data = data, columnlist = ["MFI"])

data



data


data.to_csv("./polymer_process_improvement/data/MSA_MFI_initial.csv")

