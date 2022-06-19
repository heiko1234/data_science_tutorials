



import numpy as np
import pandas as pd


import plotly.express as px


from predictive_maintenance_hd.source.data_utility import (
    split_target_and_feature,
    reset_index_train_test_split,
    scale_data,
    Encoder2DataFrame,
    remove_columns,
    check_variance
)

from predictive_maintenance_hd.source.graphics import (
    make_TSNE_plot,
    paretoplot,
    correlationplot
)



# load data



# 7 days in advanced
df = pd.read_csv("./predictive_maintenance_hd/data/df_2016_7.csv")

# 0 days in advanced
# df = pd.read_csv("./predictive_maintenance_hd/data/df_2016_0.csv")




# also use 10 days advanced data for new features

# 10 days in advanced
df_10 = pd.read_csv("./predictive_maintenance_hd/data/df_2016_10.csv")


# adding suffix to df2
df_10=df_10.add_suffix("_10")
# rephrase on name back
df_10.rename(columns={'serial_number_10':'serial_number'}, inplace=True)



# data frame for time behavior
df_merged_10 = pd.merge(df, df_10, on="serial_number")




# Feature Engineering

# some new features:   differences

for i in df_merged_10.columns:
    try:
        new_column_name = "diff_" + i
        test_i = i + "_10"
        if test_i in df_merged_10.columns:
            # print(test_i)
            df_merged_10[new_column_name] = abs(df_merged_10[test_i]-df_merged_10[i])
    except BaseException:
        pass



# 
# making the swith form df_merged_10 to df

df = df_merged_10


list_of_columns_to_drop = ['serial_number', "model", "capacity_bytes_10", "diff_failure", "failure_2", 'failure_10', 'model_10', "date_10"]

df = remove_columns(data=df, list_columns_to_remove=list_of_columns_to_drop)




# list(df.columns)


columns_to_remove = ["diff_smart_184_raw", "diff_smart_199_raw", 
    "diff_smart_183_raw", "diff_smart_189_raw", 
    "diff_smart_3_normalized", "diff_smart_188_raw"]


df = remove_columns(data=df, list_columns_to_remove=columns_to_remove)



# some overview about the data
df.describe()
df.isna().sum()
df.std()






# replace inf and drop nan values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.dropna(axis=0)




# column names

cnames=list(df.columns)
cnames




# only one model kind
list(set(list(df["model"])))    # ['ST4000DM000']





# making some plots

# colorscale=px.colors.sequential.Bluered
# colorscale=px.colors.diverging.Picnic

correlationplot(data=df, 
    colorscale=None, 
    title="Correlations", 
    hoferinfo=True, 
    digits=3, 
    annotation=False, 
    plot=True)



# makeing some plots

fig =  px.histogram(data_frame=df, x="diff_smart_9_raw", color = "failure", nbins=100, marginal="box")
fig.show()



for c_element in list(df.columns):
    fig = px.histogram(df, x=c_element)
    fig.show()




# remove boring columns


list_of_columns_to_drop = ["date", "model", "capacity_bytes", "diff_capacity_bytes"]

df = remove_columns(df, list_columns_to_remove=list_of_columns_to_drop)

df


check_variance(data=df)



# remove  

list_of_columns_to_drop = ['serial_number', 'split_serial_number_3', 'split_serial_number_4', 'split_serial_number_1']

df = remove_columns(data=df, list_columns_to_remove=list_of_columns_to_drop)


df.head()





# selection on 3 + 1 value columns, graphical evaluation
df = df.loc[:, ["diff_smart_9_raw",  "failure"]]
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





# Transformer

MinMax_transformer = MinMaxScaler(feature_range=(0, 1))

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=MinMax_transformer)



# Transformer

MinMax_transformer = StandardScaler(with_mean=True, with_std=True)

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=MinMax_transformer)





# Transformers
quantile_transformer = QuantileTransformer(random_state=0)

train_np, test_np, scaler = scale_data(train=features_train, test=features_test, scaler=quantile_transformer)







# Transformers   box-cox
powertransformer=PowerTransformer(method='box-cox', standardize=True)



def add_const(data, value=1):
    for ccol in data.columns:
        data[ccol] = data[ccol]+value
    return data



features_train_bc = add_const(data=features_train, value=1)
features_test_bc = add_const(data=features_test, value=1)

# features_train_bc
# features_test_bc


train_np, test_np, scaler = scale_data(train=features_train_bc, test=features_test_bc, scaler=powertransformer)


# End box-cox transformation




# combain train features scaled and target
# concat for plots

train_df = pd.DataFrame(data=train_np, columns=feature_names)

dd = pd.concat([train_df, target_train], axis=1)
dd



# make some plots

for c_element in list(dd.columns):
    fig =  px.histogram(data_frame=dd, x=c_element, color = "failure", nbins=100, marginal="box")
    fig.show()





# make TSNE for scaled data

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
from sklearn.dummy import DummyClassifier

from sklearn.gaussian_process.kernels import RBF







model_dict = {
    "RFC": RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    "AdaC": AdaBoostClassifier(base_estimator=None, n_estimators=50, learning_rate=1, algorithm="SAMME.R", random_state=None),
    "MLPC": MLPClassifier(alpha=1, max_iter=1000),
    "KNC": KNeighborsClassifier(n_neighbors=5),
    "DTC": DecisionTreeClassifier(max_depth=5),
    "Dummy": DummyClassifier(strategy="most_frequent")
}



from predictive_maintenance_hd.source.model_evalution import (
    model_evaluation
)


model_evaluation(model_dict, train_np, test_np, target_train, target_test)




# pic one model

key = "RFC"
model = model_dict[key]
clf=model.fit(X= train_np, y=target_train)




# # Explainability


# bring feature and target data to gether in one dataframe

test_dd = pd.concat([features_test, target_test], axis=1)
# or
train_dd = pd.concat([features_train, target_train], axis=1)





# Feature Importance

from predictive_maintenance_hd.source.feature_importance import (
    feature_importance
)
from predictive_maintenance_hd.source.graphics import (
    paretoplot
)



# training data
fi= feature_importance(trained_model=clf, df=train_dd, feature_columns=feature_names, target_column=target_name)
fi


# test data
fi= feature_importance(trained_model=clf, df=test_dd, feature_columns=feature_names, target_column=target_name)
fi


# pareto with setting varialbles

paretoplot(data=fi, column_of_names="feature", column_of_values="importance", yname="feature importance", plot=True)

# pareto with default values
paretoplot(data=fi, yname="feature importance", plot=True)








