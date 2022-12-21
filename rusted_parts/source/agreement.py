

import pandas as pd

import sklearn

from sklearn.metrics import cohen_kappa_score

# possible combinations
from itertools import combinations



def inter_rating(data, list_of_rater):
    output = []
    comb = combinations(list_of_rater, 2)

    for i in comb:
        kappa=round(cohen_kappa_score(data[i[0]], data[i[1]]),4)


        output_extend = pd.DataFrame(data=[[i[0], i[1], kappa]], columns=["rater1", "rater2", "kappa"] )
        output.append(output_extend)

    output = pd.concat(output, axis=0)
    output = output.reset_index(drop = True)

    return output


def expert_rating(data, list_of_rater, expert):

    output = []

    for i in list_of_rater:
        kappa=round(cohen_kappa_score(data[i], data[expert]),4)
        output_extend = pd.DataFrame(data=[[i, expert, kappa]], columns=["rater1", "expert", "kappa"] )
        output.append(output_extend)

    output = pd.concat(output, axis=0)
    output = output.reset_index(drop = True)

    return output


def misclassifications(data, list_of_rater, expert, part):

    output = []

    for i in list_of_rater:
        new_df = data.groupby([expert, i])[part].count()
        new_df = new_df.reset_index(drop = False)
        new_df.columns = ["Expert Rating", "Normal Rating", "Count"]
        new_df["Rater"] = i

        output.append(new_df)

    output = pd.concat(output, axis=0)
    output = output.reset_index(drop = True)

    so = output.groupby(["Expert Rating", "Normal Rating"]).sum(numeric_only=True)
    so = so.reset_index(drop = False)

    so = so[so["Normal Rating"] != so["Expert Rating"]]


    pso = so.pivot(index="Normal Rating", columns=["Expert Rating"], values = ["Count"])
    pso = pso.reset_index(drop=False)

    pso.columns = pso.columns.get_level_values(1)

    pso.reset_index()

    pso_columns = list(pso.columns)
    pso_columns[0] = "Normal Rating"
    pso.columns = pso_columns

    return pso




