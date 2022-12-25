


from source.gen_opt.setpoint_suggestion_genopt import (
    genetic_algorithm
)


import pandas as pd

from source.mlflow_expand_functions import (
    get_mlflow_model,
    #get_model_json_artifact,
    #read_model_json_from_blob,
    create_all_model_json_dict,
    flatten_dict,
    # flatten_consolidate_dict,
    #create_warning,
    decode_df_mlflow_dtype
)



Rusted_models = [
    "Rusted_Thickness",
    "Rusted_L",
    "Rusted_a",
    "Rusted_b"
]


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



def create_testdata(AT=70, DpH=5.5, DC=12.5, At=30, AC=190):

    data = pd.DataFrame(
        data=[[AT, DpH, DC, At, AC]],
        columns=[
            "Anodize Temp",
            "Dye pH",
            "Dye Conc",
            "Anodize Time",
            "Acid Conc",
        ],
    )
    data = decode_df_mlflow_dtype(data = data, dtype_dict=dtype_dict)
    return data


model_Thickness= get_mlflow_model(model_name=Rusted_models[0], azure=True)
model_L= get_mlflow_model(model_name=Rusted_models[1], azure=True)
model_a= get_mlflow_model(model_name=Rusted_models[2], azure=True)
model_b= get_mlflow_model(model_name=Rusted_models[3], azure=True)





def create_bounds_list(names_order, bounds_dict):
    return [bounds_dict[element] for element in names_order]


def bounds_dict_generator(limit_dict):
    output = {}

    for key in limit_dict.keys():
        output[key] = [limit_dict[key]["min"], limit_dict[key]["max"]]

    return output



limits_dict

# >>> limits_dict
# {'Anodize Temp': {'min': 60.0, 'max': 90.0}, 'Dye pH': {'min': 5.0, 'max': 6.5}, 'Dye Conc': {'min': 10.0, 'max': 15.0}, 'Anodize Time': {'min': 20.0, 'max': 40.0}, 'Acid Conc': {'min': 170.0, 'max': 205.0}, 'Thickness': {'min': 0.39, 'max': 1.07}, 'L*': {'min': 1.05, 'max': 21.73}, 'a*': {'min': -2.48, 'max': 7.75}, 'b*': {'min': -7.93, 'max': 2.83}}

bounds_dict = bounds_dict_generator(limits_dict)

bounds_dict 
# >>> bounds_dict 
# {'Anodize Temp': [60.0, 90.0], 'Dye pH': [5.0, 6.5], 'Dye Conc': [10.0, 15.0], 'Anodize Time': [20.0, 40.0], 'Acid Conc': [170.0, 205.0], 'Thickness': [0.39, 1.07], 'L*': [1.05, 21.73], 'a*': [-2.48, 7.75], 'b*': [-7.93, 2.83]}



# | Variable   | Target | Spez. Range |     Range    |
# ----------------------------------------------------
# | Thickness  |  0.85  |    0.15     |   1.0 - 0.7  |
# |    L*      |  9.75  |    1.75     |  11.5 - 8.0  |
# |    a*      |  1.5   |    1.5      |   3.0 - 0.0  |
# |    b*      |  0.0   |    1.5      |   1.5 - -1.5 |
# ----------------------------------------------------

create_df_testing_cnames = ["Anodize Temp", "Dye pH", "Dye Conc", "Anodize Time", "Acid Conc"]


bounds = create_bounds_list(create_df_testing_cnames, bounds_dict)

bounds
# >>> bounds
# [[60.0, 90.0], [5.0, 6.5], [10.0, 15.0], [20.0, 40.0], [170.0, 205.0]]

target_names = ["Thickness", "L*", "a*", "b*"]
target = [0.85, 9.75, 1.5, 0.0]
std_target = [0.15, 1.75, 1.5, 1.5]


def loss_function(target, X):

    idata = create_testdata(AT=X[0], DpH=X[1], DC=X[2], At=X[3], AC=X[4])
    Thickness = model_Thickness.predict(idata)[0]
    L = model_L.predict(idata)[0]
    a = model_a.predict(idata)[0]
    b = model_b.predict(idata)[0]

    diff_Thickness = abs(target[0] - Thickness) #/ std_target[0]
    diff_L = abs(target[1] - L) #/ std_target[1]
    diff_a = abs(target[2] - a) #/ std_target[2]
    diff_b = abs(target[3] - b) #/ std_target[3]

    return diff_Thickness+diff_L+diff_a+diff_b



new_setpoints = genetic_algorithm(
    objective=loss_function,
    target=target,
    bounds=bounds,
    break_accuracy=0.005,
    digits=5,
    n_bits=16,
    n_iter=30,
    n_pop=100,
    r_cross=0.9,
    r_mut=None,
)
new_setpoints


# >>> new_setpoints
# [76.875, 5.59777, 11.26228, 37.19238, 204.93858]


# ["Anodize Temp", "Dye pH", "Dye Conc", "Anodize Time", "Acid Conc"]


# These data
testdata = create_testdata(AT=79.5, DpH=6.3, DC=11.2, At=39.6, AC=204.4)

# or these data
testdata= create_testdata(AT=new_setpoints[0], DpH=new_setpoints[1], DC=new_setpoints[2], At=new_setpoints[3], AC=new_setpoints[4])
testdata["Thickness_pred"]= model_Thickness.predict(testdata)
testdata["L_pred"]= model_L.predict(testdata)
testdata["a_pred"]= model_a.predict(testdata)
testdata["b_pred"]= model_b.predict(testdata)


testdata

# >>> testdata
#    Anodize Temp   Dye pH  Dye Conc  Anodize Time   Acid Conc  Thickness_pred    L_pred    a_pred    b_pred
# 0            76  5.59777  11.26228            37  204.938583        0.707302  9.719687  1.502779 -0.194312


# | Variable   | Target | Spez. Range |     Range    |
# ----------------------------------------------------
# | Thickness  |  0.85  |    0.15     |   1.0 - 0.7  |
# |    L*      |  9.75  |    1.75     |  11.5 - 8.0  |
# |    a*      |  1.5   |    1.5      |   3.0 - 0.0  |
# |    b*      |  0.0   |    1.5      |   1.5 - -1.5 |
# ----------------------------------------------------

