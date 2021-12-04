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

    SA2 = SA * SA
    SA3 = SA * SA * SA
    Xf2 = Xf * Xf
    data_list = [[M_per, Xf, SA, SA2, SA3, Xf2]]

    data = pd.DataFrame(
        data=data_list, columns=["M%", "Xf", "SA", "SASA", "SASASA", "XfXf"]
    )

    for cname in data.columns:
        try:
            data[cname] = data[cname].astype("float32")
        except BaseException:
            continue

    return data


def create_bounds_list(names_order, bounds_dict):
    return [bounds_dict[element] for element in names_order]





data = pd.read_csv("./polymer_process_improvement/data/CrisisTeamData.csv", sep=",")

data.head()

data = data.iloc[:, 1:]



data["select"] = 1

data.loc[data["Yield"] <= 85.0, "select"] = 0

data


fig = px.histogram(
    data, x="Yield", marginal="box", color="select", hover_data=data.columns, nbins=30
)
fig.show()

fig = px.histogram(
    data, x="MFI", marginal="box", color="select", hover_data=data.columns, nbins=30
)
fig.show()

fig = px.histogram(
    data, x="CI", marginal="box", color="select", hover_data=data.columns, nbins=30
)
fig.show()


