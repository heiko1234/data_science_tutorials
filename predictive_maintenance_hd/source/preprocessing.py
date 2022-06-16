



import numpy as np
import pandas as pd

import plotly.express as px


from sklearn.dummy import DummyClassifier
from sklearn.metrics import balanced_accuracy_score

from predictive_maintenance_hd.source.utility import (
    split_target_and_feature,
    reset_index_train_test_split,
    scale_data
)

from predictive_maintenance_hd.source.make_TSNE import (
    make_TSNE_plot
)

from predictive_maintenance_hd.source.utility import (
    Encoder2DataFrame
)




# load data

df = pd.read_csv("./predictive_maintenance_hd/data/df_2016_7.csv")



cnames=list(df.columns)
cnames


df.shape  #9551, 27
list(df.columns)


df.describe()

df.isna().sum()
df.std()


# replace inf 
df.replace([np.inf, -np.inf], np.nan, inplace=True)

df = df.dropna(axis=0)



# fig = px.histogram(df, x="model")
# fig.show()

list(set(list(df["model"])))    # ['ST4000DM000']


# fig = px.histogram(df, x="serial_number")
# fig.show()






# Feature Engineering

df["split_serial_number_3"] = df["serial_number"].str[:3]
df["split_serial_number_4"] = df["serial_number"].str[:4]
df["split_serial_number_1"] = df["serial_number"].str[:1]


# makeing some plots

fig =  px.histogram(data_frame=df, x="split_serial_number_4", color = "failure", nbins=100, marginal="box")
fig.show()



for c_element in list(df.columns):
    fig = px.histogram(df, x=c_element)
    fig.show()



# remove date column, as loop
list_of_columns_to_drop = ["date", "model", "capacity_bytes"]
for i in list_of_columns_to_drop:
    try: 
        df = df.drop(i, axis=1)
    except BaseException:
        df = df



# be sure date is out of df
df = df.drop("date", axis=1)

df.head()

list(df.columns)
df.shape  #9551, 28





#  One Hot Encoder for the serial number codation


cnames_serial = [i for i in df.columns if "serial" in i]
cnames_serial





# serial_number encoding

cnames_serial




dd_extra1, ohe1 = Encoder2DataFrame(data=df, column_name="split_serial_number_1")
dd_extra1.head()


dd_extra3, ohe3 = Encoder2DataFrame(data=df, column_name="split_serial_number_3")
dd_extra3.head()

dd_extra4, ohe4 = Encoder2DataFrame(data=df, column_name="split_serial_number_4")
dd_extra4.head()


# list(dd_extra1.columns)
# list(dd_extra3.columns)
# list(dd_extra4.columns)


# new_df
new_df = pd.concat([df, dd_extra1, dd_extra3, dd_extra4], axis=1)
new_df


# list(new_df.columns)


# rephrase new_df  to   df

# db = df


db = new_df



# be sure date is out of df
# remove date serial_number columns
cnames_serial
list_of_columns_to_drop = ['serial_number', 'split_serial_number_3', 'split_serial_number_4', 'split_serial_number_1']

for i in list_of_columns_to_drop:
    try: 
        db = db.drop(i, axis=1)
    except BaseException:
        db = db

db.head()






# Split date in feature and target data

data_target, data_features, target_name, feature_names = split_target_and_feature(data=db, target="failure")


# split features and target data in train and test datasets

features_train, features_test, target_train, target_test = reset_index_train_test_split(
    feature_data=data_features, 
    target_data=data_target, 
    test_size=0.2, 
    random_state=2022
    )

list(features_train.columns)


# Create a dummy classifier model


DC = DummyClassifier(strategy="most_frequent")
clf=DC.fit(X= features_train, y=target_train)


dummy_train=clf.score(features_train, target_train)
dummy_test=clf.score(features_test, target_test)

dummy_bas_train=balanced_accuracy_score(target_train, clf.predict(features_train))
dummy_bas_test=balanced_accuracy_score(target_test, clf.predict(features_test))

dummy_train   # 0.912
dummy_test    # 0.914
dummy_bas_train   # 0.5
dummy_bas_test    # 0.5



#t-sne

make_TSNE_plot(
    features=features_train, 
    target=target_train, 
    plot=True)




# Data Preprocessing

from sklearn.preprocessing import (
    PowerTransformer,
    QuantileTransformer,
    StandardScaler,
    MinMaxScaler,
)



# target_test
# target_train


# Transformers
quantile_transformer = QuantileTransformer(random_state=0)

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=quantile_transformer)



# box-cox
powertransformer=PowerTransformer(method='box-cox', standardize=True)


features_train
features_test


def add_const(data, value=1):
    for ccol in data.columns:
        data[ccol] = data[ccol]+value
    return data



features_train_bc = add_const(data=features_train, value=1)
features_test_bc = add_const(data=features_test, value=1)

features_train_bc
features_test_bc


train_np, test_np, scaler = scale_data(train=features_train_bc, test=features_test_bc, scaler=powertransformer)



# combain train features scaled and target

train_df = pd.DataFrame(data=train_np, columns=feature_names)

dd = pd.concat([train_df, target_train], axis=1)
dd


for c_element in list(dd.columns):
    fig =  px.histogram(data_frame=dd, x=c_element, color = "failure", nbins=100, marginal="box")
    fig.show()




make_TSNE_plot(
    features=train_np, 
    target=target_train, 
    plot=True)





# classification models

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.gaussian_process.kernels import RBF


model_names = [
    "RFC", 
    "AdaC", 
    "MLPC", 
    "KNC", 
    "DTC"
    ]


classifiers = [
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    MLPClassifier(alpha=1, max_iter=1000),
    KNeighborsClassifier(3),
    DecisionTreeClassifier(max_depth=5),
]


output_df = pd.DataFrame(columns=["model_name", "r2_train", "r2_test", "bas_train", "bas_test"])
output_df


for count, value in enumerate(model_names):

    print(f"count: {count}")


    model = classifiers[count]
    clf=model.fit(X= train_np, y=target_train)

    r2_train=clf.score(train_np, target_train)  
    r2_test=clf.score(test_np, target_test) 

    bas_train=balanced_accuracy_score(target_train, clf.predict(train_np)) 
    bas_test=balanced_accuracy_score(target_test, clf.predict(test_np)) 

    dict = {"model_name": value,
            "r2_train": r2_train,
            "r2_test": r2_test,
            "bas_train": bas_train,
            "bas_test": bas_test
        }

    output_df = output_df.append(dict, ignore_index = True)

    print(output_df)



# add dummy classifier

dict = {"model_name": "dummyCLF",
        "r2_train": dummy_train,
        "r2_test": dummy_test,
        "bas_train": dummy_bas_train,
        "bas_test": dummy_bas_test
    }

output_df = output_df.append(dict, ignore_index = True)



output_df


