

import pandas as pd
import numpy as np
import plotly.express as px



data = pd.read_csv("./polymer_process_improvement/data/CrisisTeamData.csv", sep=",")

data.head()

data = data.iloc[:,1:]

data["SASA"] = data["SA"]**2
data["SASASA"] = data["SA"]**3
data["XfXf"] = data["Xf"]**2

data_filtered = data[data["Yield"] >=55.0]

data_filtered.to_parquet("./polymer_process_improvement/data/CrisisTeamData.parquet")


data["select"] = 1

data.loc[data["Yield"] <= 55.0, "select"] = 0

data


fig = px.histogram(data, x="Yield", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()

fig = px.histogram(data, x="MFI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()

fig = px.histogram(data, x="CI", marginal="box", color = "select", hover_data=data.columns, nbins = 30)
fig.show()





import mlflow
import os
from pathlib import PurePosixPath
# from pathlib import Path
import pickle
from dotenv import load_dotenv

load_dotenv()


local_run = os.getenv("LOCAL_RUN", False)





def get_mlflow_model(model_name, azure=True, model_dir = "/model/"):

    if azure:
        model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:/")
        model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
        artifact_path = PurePosixPath(model_dir).joinpath(model_name, model_stage)
        artifact_path

        model = mlflow.pyfunc.load_model(str(artifact_path))
        print(f"Model {model_name} loaden from Azure: {artifact_path}")

    if not azure:
        model = pickle.load(open(f"{model_dir}/{model_name}/model.pkl", 'rb'))
        print(f"Model {model_name} loaded from local pickle file")

    return model





MFI_model = get_mlflow_model(model_name = "MFI_polymer", azure=True, model_dir = None)

CI_model = get_mlflow_model(model_name = "CI_polymer", azure=True, model_dir = None)



for cname in data.columns:
    try: 
        data[cname] = data[cname].astype("float32")
    except BaseException:
        continue

data

data["prediction"] = MFI_model.predict(data)

data["diff"] = data["MFI"]-data["prediction"]


fig = px.scatter(data, x = "Batch_number", y = "diff")
fig.show()

fig = px.scatter(data, x = "MFI", y = "prediction", color = "select")
fig.show()


data.corr()["diff"]



data["CI_prediction"] = CI_model.predict(data)

data["CI_diff"] = data["CI"]-data["CI_prediction"]

data["CI_model_diff"] = 0
data.loc[data["CI_diff"] <= -30, "CI_model_diff"] = 1
data.loc[data["CI_diff"] >= 30, "CI_model_diff"] = 1

fig = px.scatter(data, x = "CI", y = "CI_diff", color = "CI_model_diff")
fig = px.scatter(data, x = "CI", y = "CI_prediction", color = "CI_model_diff")
fig.show()

data[data["CI_model_diff"] == 1]

data.corr()["CI_model_diff"]



fig = px.scatter(data, x ="SA", y = "Yield", color = "CI_model_diff")
fig.show()





def create_df_testing(M_per = 1, Xf = 1, SA= 1):

    SA2 = SA*SA
    SA3 = SA*SA*SA
    Xf2 = Xf*Xf
    data_list = [[M_per, Xf, SA, SA2, SA3, Xf2]]
    
    data = pd.DataFrame(data=data_list, columns = ["M%", "Xf", "SA", "SASA", "SASASA", "XfXf"] )

    for cname in data.columns:
        try: 
            data[cname] = data[cname].astype("float32")
        except BaseException:
            continue
    
    return data


create_df_testing(M_per = 1, Xf = 1, SA = 1)





# objective function
def loss_MFI_function(target, X):
    model = MFI_model
    M_per=X[0]
    Xf=X[1]
    SA=X[2]
    idata = create_df_testing(M_per, Xf, SA)
    modeloutput = model.predict(idata)
    diff = abs(target-modeloutput)
    return diff


# loss_MFI_function(target=205, X=[2, 10, 60])  #3.176


def create_bounds_list(names_order, bounds_dict):
    return [bounds_dict[element] for element in names_order]



from polymer_process_improvement.source.setpoint_suggestion_genopt import genetic_algorithm


bounds_dict = {"Xf": [9.6, 22.2], "SA": [50.1, 79.7], "M_per": [0, 3.6]}   #out of mlflow
create_df_testing_cnames = ["M_per", "Xf", "SA"]


bounds = create_bounds_list(create_df_testing_cnames, bounds_dict)

target = 204


new_setpoints = genetic_algorithm(objective=loss_MFI_function, target=target, bounds =bounds, break_accuracy=0.005, n_bits=16, n_iter=100, n_pop=100, r_cross=0.9, r_mut=None)
#new_setpoints

MFI_model.predict(create_df_testing(M_per = new_setpoints[0], Xf = new_setpoints[1], SA= new_setpoints[2]))[0]





