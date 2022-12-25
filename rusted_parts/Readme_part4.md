
# Modelling

## DOE Design

We plan a Doe experiment and will set the limits for this as we have seen from the specifications.

```bash

| Variable   | Target | Spez. Range |     Range    |
----------------------------------------------------
| Thickness  |  0.85  |    0.15     |   1.0 - 0.7  |
|    L*      |  9.75  |    1.75     |  11.5 - 8.0  |
|    a*      |  1.5   |    1.5      |   3.0 - 0.0  |
|    b*      |  0.0   |    1.5      |   1.5 - -1.5 |
----------------------------------------------------

```


## Modelling

### MLFLow

We stay with the MLOps Approach and will train several models for:
- Thickness
- L*
- a*
- b*

with the script for MLFlow. 

We only need to change the trainings.yaml file

```bash
# in    training_config.yaml

data_load: "/home/heiko/Repos/Playground/multi_vari_msa/data/Anodize_CustomDesign_DOE_Results.parquet"

###########
# Target: #
###########

# target: "Thickness"   # select on of the targets and pic the correct name :)
target: "L*"
# target: "b*"
# target: "a*"


features:
  - "Anodize Temp"
  - "Dye pH"
  - "Dye Conc"
  - "Anodize Time"
  - "Acid Conc"


MLFlow: True # False #True

# MLFlow_Experiment: "Rusted_Thickness"   # select on of the MLFlow names
MLFlow_Experiment: "L_rusted"
# MLFlow_Experiment: "b_rusted"
# MLFlow_Experiment: "a_rusted"


test_split:
  test_size: 0.3     # less data points, otherwise it gives an error :)
  random_state: 2021


```


Please change the inputs for `MLFlow_Experiment` and `target` and run it several times. 


After we made all for runs we can see in MLFlow (localhost:5000) the models. For each Target its own Experiment with at least 15 different models, with or without a scaler, simple or complex models and their performance as matrics.

![mlflow_screen](./assets/MLFlow_screen.png)


### Next Steps

We need to select a model to make it a model and then we need to stage it.

I call my models:

- Rusted_Thickness
- Rusted_L
- Rusted_a
- Rusted_b

to make it very simple i also use the linear regression models as registered models.


![mlflow_register](./assets/mlflow_register.png)
![mlflow_stageit](./assets/mlflow_stageit.png)


### Small Commment
Version Conrol of MLFlow, pandas and numpy is everything. I had a few problems and stayed with the old configuration of:

```bash

[tool.poetry.dependencies]
python = ">=3.8.1,<3.9"
pandas = "^1.5.2"
numpy = "<=1.21.3"   # else mlflow is not working
plotly = "^5.11.0"
openpyxl = "^3.0.10"
statsmodels = "^0.13.5"
scikit-learn = "*"
mlflow = "1.14.1"
protobuf = "<3.20"   # else mlfow is not working

azure-storage-blob = "==12.7.1"
azure-identity ="^1.7.0"

```

Just in case it got lost :)


## Working with the Models

The best way to gain knowledge and to work with these models is to have an interface to these models. 

We as data scientist can directly use the models out of MLFlow but what is the best way for non-data scientists?
How should we provide someone these models and the hidden informations in the crosslinking of all models?


[Here](./source/mlflow_expand_functions.py) and [here](./source/usage_mlflow_expand_functions.py) are some functions to to get the informations from your local mlflow server and to work with them.

I guess this is already nice but not sufficient for a workflow that we like to have and which is maybe available in proffesional software solutions like `JMP`, `matlab`, `origin` and co.


```bash

import pandas as pd

from source.mlflow_expand_functions import (
    get_mlflow_model,
    get_model_json_artifact,
    read_model_json_from_blob,
    create_all_model_json_dict,
    flatten_dict,
    flatten_consolidate_dict,
    create_warning,
    decode_df_mlflow_dtype
)


# models:  
# Rusted_Thickness
# Rusted_L
# Rusted_a
# Rusted_b


Rusted_models = [
    "Rusted_Thickness",
    "Rusted_L",
    "Rusted_a",
    "Rusted_b"
]



model_Thickness= get_mlflow_model(model_name=Rusted_models[0], azure=True)


# for one model
model_featues=get_model_json_artifact(
                    azure=True,
                    path=None,
                    model_name=Rusted_models[0],
                    features="feature_limits.json",
                )
model_featues


model_dtypes=get_model_json_artifact(
                    azure=True,
                    path=None,
                    model_name=Rusted_models[0],
                    features="feature_dtype.json",
                )
model_dtypes


# or for all models
feature_dtypes_dict = create_all_model_json_dict(local=False,
    list_of_models=Rusted_models,
    features="feature_dtypes.json")
feature_dtypes_dict


feature_limits_dict = create_all_model_json_dict(local=False,
    list_of_models=Rusted_models,
    features="feature_limits.json")
feature_limits_dict


# for all the data types
dtype_dict=flatten_dict(nested_dict=feature_dtypes_dict)
dtype_dict

# for all the limits
limits_dict=flatten_dict(nested_dict=feature_limits_dict)
limits_dict


AT = 70   # 60..90
DpH = 5.5   #5.0 .. 6.5
DC = 12.5   # 10.0 .. 12.5
AT = 30    # 20..30
AC = 190   # 170..205


data = pd.DataFrame(
    data=[[AT, DpH, DC, AT, AC]],
    columns=[
        "Anodize Temp",
        "Dye pH",
        "Dye Conc",
        "Anodize Time",
        "Acid Conc",
    ],
)
data

data = decode_df_mlflow_dtype(data = data, dtype_dict=dtype_dict)

data

Rusted_models = [
    "Rusted_Thickness",
    "Rusted_L",
    "Rusted_a",
    "Rusted_b"
]


model_Thickness= get_mlflow_model(model_name=Rusted_models[0], azure=True)
model_L= get_mlflow_model(model_name=Rusted_models[1], azure=True)
model_a= get_mlflow_model(model_name=Rusted_models[2], azure=True)
model_b= get_mlflow_model(model_name=Rusted_models[3], azure=True)


model_Thickness.predict(data)[0]
model_L.predict(data)[0]
model_a.predict(data)[0]
model_b.predict(data)[0]

```


## Knowledge

How to we extract knowledge out of the models? 

How to interactively interact with the models?

Can we make an app for this?


[Part5](./Readme_part5.md)