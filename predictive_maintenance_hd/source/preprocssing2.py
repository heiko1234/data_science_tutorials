

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

from predictive_maintenance_hd.source.pareto_plot import (
    correlationplot
)




df = pd.read_csv("./predictive_maintenance_hd/data/df_2016_7.csv")

df2 = pd.read_csv("./predictive_maintenance_hd/data/df_2016_10.csv")


# colorscale=px.colors.diverging.Picnic
# colorscale=px.colors.sequential.Bluered,

correlationplot(data=df2, colorscale=None, title="Correlations", hoferinfo=True, digits=3, annotation=False, plot=True)






# adding suffix to df2
df2=df2.add_suffix("_10")


# rephrase on name back
df2.rename(columns={'serial_number_10':'serial_number'}, inplace=True)

list(df.columns)
list(df2.columns)

dd = pd.merge(df, df2, on="serial_number")
dd

df.shape  #9551, 27
dd.shape  #9551, 53


df = dd

# remove date column, as loop
list_of_columns_to_drop = ["date", "date_10", "capacity_bytes"]
for i in list_of_columns_to_drop:
    try: 
        df = df.drop(i, axis=1)
    except BaseException:
        df = df


# some ne features

for i in dd.columns:
    try:
        new_column_name = "diff_" + i
        test_i = i + "_10"
        if test_i in dd.columns:
            print(test_i)
            df[new_column_name] = abs(df[test_i]-df[i])
    except BaseException:
        pass




df.shape


list_of_columns_to_drop = ['serial_number', "model", "capacity_bytes_10", "diff_failure", "failure_2", 'failure_10', 'model_10']

for i in list_of_columns_to_drop:
    try: 
        df = df.drop(i, axis=1)
    except BaseException:
        df = df


#all values absolute
# df = abs(df)

df.columns

# df["diff_smart_1_raw"].std()
# df["diff_smart_5_raw"].std()


def check_variance(data):
    for i in data.columns:
        if data[i].std() < 0.01:
            print(f"{i}: {data[i].std()}")



df.shape # 9551, 67
check_variance(data=df)



df = df.drop(columns=["diff_smart_184_raw", "diff_smart_199_raw", "diff_smart_183_raw", "diff_smart_189_raw", "diff_smart_3_normalized"])

df = df.drop(columns=["diff_smart_188_raw"])


df.shape   #9551, 61


# plot all

for c_element in list(df.columns):
    fig = px.histogram(df, x=c_element, color = "failure", nbins=100, marginal="box")
    fig.show()



# selection on 3 + 1 value columns, graphical evaluation
df = df.loc[:, ["diff_smart_9_raw", "diff_smart_241_raw", "diff_smart_1_raw", "failure"]]
df


# Split date in feature and target data

data_target, data_features, target_name, feature_names = split_target_and_feature(data=df, target="failure")


# split features and target data in train and test datasets

features_train, features_test, target_train, target_test = reset_index_train_test_split(
    feature_data=data_features, 
    target_data=data_target, 
    test_size=0.2, 
    random_state=2022
    )

list(features_train.columns)





make_TSNE_plot(
    features=features_train, 
    target=target_train, 
    plot=True)




from sklearn.preprocessing import (
    PowerTransformer,
    QuantileTransformer,
    StandardScaler,
    MinMaxScaler,
)



# box-cox
powertransformer=PowerTransformer(method='box-cox', standardize=True)



def add_const(data, value=1):
    for ccol in data.columns:
        data[ccol] = data[ccol]+value
    return data



features_train_bc = add_const(data=features_train, value=1)
features_test_bc = add_const(data=features_test, value=1)


check_variance(data=features_train_bc)
check_variance(data=features_test_bc)
# features_train_bc
# features_test_bc


train_np, test_np, scaler = scale_data(train=features_train_bc, test=features_test_bc, scaler=powertransformer)





make_TSNE_plot(
    features=train_np, 
    target=target_train, 
    plot=True)




# Transformers
quantile_transformer = QuantileTransformer(random_state=0)

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=quantile_transformer)


make_TSNE_plot(
    features=train_np, 
    target=target_train, 
    plot=True)




# Transformer

MinMax_transformer = MinMaxScaler()

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=MinMax_transformer)




# classification models

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import balanced_accuracy_score


from sklearn.gaussian_process.kernels import RBF


model_names = [
    "RFC", 
    "AdaC", 
    "MLPC", 
    "KNC", 
    "DTC",
    "Dummy"
    ]


classifiers = [
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    MLPClassifier(alpha=1, max_iter=1000),
    KNeighborsClassifier(3),
    DecisionTreeClassifier(max_depth=5),
    DummyClassifier(strategy="most_frequent")
]


output_df = pd.DataFrame(columns=["model_name", "r2_train", "r2_test", "bas_train", "bas_test"])
output_df


count = 0
value = "RFC"


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




count = 0
value = "RFC"

model = classifiers[count]
clf=model.fit(X= train_np, y=target_train)




# # Explainability

test_dd = pd.concat([features_test, target_test], axis=1)
# or
test_dd = pd.concat([features_train, target_train], axis=1)
test_dd

feature_names
target_name




# Feature Importance

from predictive_maintenance_hd.source.feature_importance import (
    feature_importance
)

from predictive_maintenance_hd.source.pareto_plot import (
    paretoplot
)



fi= feature_importance(trained_model=clf, df=test_dd, feature_columns=feature_names, target_column=target_name)
fi


paretoplot(data=fi, column_of_names="feature", column_of_values="importance", yname="feature importance", plot=True)

paretoplot(data=fi, yname="feature importance", plot=True)





