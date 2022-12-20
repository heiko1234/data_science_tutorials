


import pandas as pd

from rusted_parts.source.multi_vari import (
    make_muti_vari_plot,
    multi_vari_plot
)


thickness_data = pd.read_excel("./rusted_parts/data/Thickness_MSA.xlsx")

data = thickness_data

data




make_muti_vari_plot(
    data=thickness_data,
    operator="Operator",
    part="Part",
    parameter="Thickness",
    )



make_muti_vari_plot(
    data=thickness_data,
    operator="Operator",
    part="Part",
    parameter="Thickness",
    type="mean"
    )



make_muti_vari_plot(
    data=thickness_data,
    operator="Operator",
    part="Part",
    parameter="Thickness",
    type="std"
    )



multi_vari_plot(data=data,
    operator="Operator",
    part="Part",
    parameter="Thickness",
    plot=True
    )


# ############



data = thickness_data.groupby(["Part", "Operator"]).mean(numeric_only=True)
data = data.reset_index(drop = False)
data


data = thickness_data.groupby(["Part", "Operator"]).std(numeric_only=True)
data = data.reset_index(drop = False)
data



multi_vari_plot(data=data,
    operator="Operator",
    part="Part",
    parameter="Thickness"
    )


