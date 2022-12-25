
import pandas as pd

from src.with_mlflow.mlflow_expand_functions import (
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



create_warning(TAG_limit_dict=get_model_json_artifact(model_name= Rusted_models[0], features="feature_limits.json"), key = "Anodize Temp", value=4) #yes


# Load and make it MLFlow compatible
data = pd.read_excel("./data/Anodize_CustomDesign_DOE_Results.xlsx")
data
data = decode_df_mlflow_dtype(data = data, dtype_dict=dtype_dict)
data
data["L_pred"]= model_L.predict(data)
data["a_pred"]= model_a.predict(data)
data["b_pred"]= model_b.predict(data)
data["Thickness_pred"]= model_Thickness.predict(data)

data





