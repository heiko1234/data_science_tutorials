

import pandas as pd
import numpy as np
import plotly.express as px



data = pd.read_csv("./polymer_process_improvement/data/CrisisTeamData.csv", sep=",")

data.head()

data = data.iloc[:,1:]

data["SASA"] = data["SA"]**2
data["XfXf"] = data["Xf"]**2

data.to_parquet("./polymer_process_improvement/data/CrisisTeamData.parquet")


data["select"] = 1

data.loc[data["Yield"] <= 85.0, "select"] = 0

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
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("BLOB_MODEL_CONTAINER_NAME")




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







