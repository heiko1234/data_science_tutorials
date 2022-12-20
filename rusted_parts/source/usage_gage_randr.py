


import pandas as pd


from rusted_parts.source.Gage_RandR import (
    gagernr,
    plot_on_groups
)


thickness_data = pd.read_excel("./data/Thickness_MSA.xlsx")

data = thickness_data

data.columns

data



operator="Operator"
instrument=None
part="Part"
result="Thickness"



plot_on_groups(data = data, x = part, y = result, color=operator, analysis = "mean")


gagernr(data=data, operator=operator, instrument = instrument, part= part, result=result)




