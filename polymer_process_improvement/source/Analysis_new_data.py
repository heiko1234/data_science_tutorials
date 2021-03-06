


import pandas as pd
import numpy as np
import plotly.express as px

import mlflow
import os
from pathlib import PurePosixPath

# from pathlib import Path
import pickle
from dotenv import load_dotenv

load_dotenv()



def get_mlflow_model(model_name, azure=True, model_dir="/model/"):

    if azure:
        model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:/")
        model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
        artifact_path = PurePosixPath(model_dir).joinpath(model_name, model_stage)
        artifact_path

        model = mlflow.pyfunc.load_model(str(artifact_path))
        print(f"Model {model_name} loaden from Azure: {artifact_path}")

    if not azure:
        model = pickle.load(open(f"{model_dir}/{model_name}/model.pkl", "rb"))
        print(f"Model {model_name} loaded from local pickle file")

    return model


def create_df_testing(M_per=1, Xf=1, SA=1):

    SA2 = SA**2
    SA3 = SA**3
    Xf2 = Xf**2
    Xf3 = Xf**3
    data_list = [[M_per, Xf, SA, SA2, SA3, Xf2, Xf3]]

    data = pd.DataFrame(
        data=data_list, columns=["M%", "Xf", "SA", "SASA", "SASASA", "XfXf", "XfXfXf"]
    )

    for cname in data.columns:
        try:
            data[cname] = data[cname].astype("float32")
        except BaseException:
            continue

    return data


def create_bounds_list(names_order, bounds_dict):
    return [bounds_dict[element] for element in names_order]




# local_run = os.getenv("LOCAL_RUN", False)



data = pd.read_csv("./polymer_process_improvement/data/VSSTeamData.csv")

data.head()

data = data.iloc[:, 1:]

data["SASA"] = data["SA"] ** 2
data["SASASA"] = data["SA"] ** 3
data["XfXf"] = data["Xf"] ** 2
data["XfXfXf"] = data["Xf"] ** 3

data_filtered = data[data["Yield"] >= 55.0]

data_filtered.to_parquet("./polymer_process_improvement/data/VSSTeamData.parquet")


data["select"] = 0

data.loc[data["Yield"] <= 55.0, "select"] = 1

data

#
list((data["MFI"] < 192) | (data["CI"] < 80))

#
data.loc[data["MFI"] < 192, "select"] = 1
data.loc[data["MFI"] > 198, "select"] = 1
data.loc[data["CI"] < 80, "select"] = 1
data

data[data["select"]==1].count()  #76
data[data["select"]==0].count()  #34


fig = px.histogram(data, x="Yield", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


fig = px.histogram(data, x="MFI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


fig = px.histogram(data, x="CI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()


data.columns
fig = px.scatter(data, x = "Batch Number", y = "CI", )
fig.show()



data["yield_selection"]= 0
data.loc[data["Yield"] < 60, "yield_selection"] = 1

fig = px.scatter(data, x = "MFI", y = "Yield", color = "yield_selection")
fig.show()

fig = px.scatter(data, x = "CI", y = "Yield", color = "yield_selection")
fig.show()


fig = px.scatter(data, x = "Xf", y = "CI", color = "yield_selection")
fig.show()


# create models with sklean to mlflow thing





# Load models


MFI_model = get_mlflow_model(model_name="MFI_polymer", azure=True, model_dir=None)

CI_model = get_mlflow_model(model_name="CI_polymer", azure=True, model_dir=None)




### Do somethng with the model

for cname in data.columns:
    try:
        data[cname] = data[cname].astype("float32")
    except BaseException:
        continue

data

data["prediction"] = MFI_model.predict(data)

data["diff"] = data["MFI"] - data["prediction"]


fig = px.scatter(data, x="MFI", y="diff", color="select")
fig.show()

fig = px.scatter(data, x="MFI", y="prediction", color="select")
fig.show()


data.corr()["diff"]


data["CI_prediction"] = CI_model.predict(data)

data["CI_diff"] = data["CI"] - data["CI_prediction"]

data["CI_model_diff"] = 0
data.loc[data["CI_diff"] <= -30, "CI_model_diff"] = 1
data.loc[data["CI_diff"] >= 30, "CI_model_diff"] = 1

fig = px.scatter(data, x="CI", y="CI_diff", color="CI_model_diff")
fig = px.scatter(data, x="CI", y="CI_prediction", color="CI_model_diff")
fig.show()

data[data["CI_model_diff"] == 1]

data.corr()["CI_model_diff"]


fig = px.scatter(data, x="SA", y="Yield", color="CI_model_diff")
fig.show()


# create_df_testing(M_per = 1, Xf = 1, SA = 1)


# objective function
def loss_MFI_function(target, X):
    model = MFI_model
    M_per = X[0]
    Xf = X[1]
    SA = X[2]
    idata = create_df_testing(M_per, Xf, SA)
    modeloutput = model.predict(idata)
    diff = abs(target - modeloutput)
    return diff


# loss_MFI_function(target=205, X=[2, 10, 60])  #3.176


from polymer_process_improvement.source.setpoint_suggestion_genopt import (genetic_algorithm)


bounds_dict = {
    "Xf": [13.45, 18.4],
    "SA": [52, 79.7],
    "M_per": [0, 3.6],
}  # out of mlflow
create_df_testing_cnames = ["M_per", "Xf", "SA"]


bounds = create_bounds_list(create_df_testing_cnames, bounds_dict)

target = 196


new_setpoints = genetic_algorithm(
    objective=loss_MFI_function,
    target=target,
    bounds=bounds,
    break_accuracy=0.005,
    n_bits=16,
    n_iter=100,
    n_pop=100,
    r_cross=0.9,
    r_mut=None,
)
new_setpoints


MFI_model.predict(create_df_testing(M_per=new_setpoints[0], Xf=new_setpoints[1], SA=new_setpoints[2]))[0]


####

# Mutli parameter

# objective function
def loss_MFI_function(target, X):

    M_per = X[0]
    Xf = X[1]
    SA = X[2]
    idata = create_df_testing(M_per, Xf, SA)
    modeloutput_MFI = MFI_model.predict(idata)
    modeloutput_CI = CI_model.predict(idata)

    diff = abs(target[0] - modeloutput_MFI)
    diff2 = abs(target[1] - modeloutput_CI)
    return 2*diff+diff2


bounds_dict = {
    "Xf": [13.45, 18.4],
    "SA": [52, 79.7],
    "M_per": [0, 3.6],
}  # out of mlflow
create_df_testing_cnames = ["M_per", "Xf", "SA"]


bounds = create_bounds_list(create_df_testing_cnames, bounds_dict)
bounds

target = [196, 90]


new_setpoints = genetic_algorithm(
    objective=loss_MFI_function,
    target=target,
    bounds=bounds,
    break_accuracy=0.005,
    n_bits=16,
    n_iter=100,
    n_pop=100,
    r_cross=0.9,
    r_mut=None,
)
new_setpoints # 1.614, 17.87, 65.15  #0.22148, 14.188, 70,318



MFI_model.predict(create_df_testing(M_per=new_setpoints[0], Xf=new_setpoints[1], SA=new_setpoints[2]))[0]
#MFI = 196.8

CI_model.predict(create_df_testing(M_per=new_setpoints[0], Xf=new_setpoints[1], SA=new_setpoints[2]))[0]
#CI = 98.4

new_setpoints= [1.614, 17.87, 65.15]
loss_MFI_function(target=[196, 90], X =new_setpoints)

MFI_model.predict(create_df_testing(M_per=new_setpoints[0], Xf=new_setpoints[1], SA=new_setpoints[2]))[0]
CI_model.predict(create_df_testing(M_per=new_setpoints[0], Xf=new_setpoints[1], SA=new_setpoints[2]))[0]

