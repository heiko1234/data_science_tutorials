

import pandas as pd

from rusted_parts.source.agreement import (
    inter_rating,
    expert_rating,
    misclassifications
)


data = pd.read_excel("./data/AttributeMSA.xlsx")

data

#     Day  Part           Hal         Carly          Jake Expert Rating
# 0     1    30  Normal Black  Smutty Black  Smutty Black  Smutty Black
# 1     1    37  Smutty Black  Smutty Black  Smutty Black  Smutty Black
# 2     1    14  Purple/Black  Purple/Black  Purple/Black  Purple/Black


data.columns
# Index(['Day', 'Part', 'Hal', 'Carly', 'Jake', 'Expert Rating'], dtype='object')

list_of_raters= ["Hal", "Carly", "Jake"]




inter_rating(data=data, list_of_rater=list_of_raters)

expert_rating(data = data, list_of_rater=list_of_raters, expert="Expert Rating")

misclassifications(data=data, list_of_rater=list_of_raters, expert="Expert Rating", part="Part")


list_of_raters2= ["Hal"]

misclassifications(data=data, list_of_rater=list_of_raters2, expert="Expert Rating", part="Part")

list_of_raters3= ["Carly"]

misclassifications(data=data, list_of_rater=list_of_raters3, expert="Expert Rating", part="Part")


