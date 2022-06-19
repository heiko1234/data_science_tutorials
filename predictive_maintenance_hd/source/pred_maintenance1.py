



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
# df_10 = pd.read_csv("./predictive_maintenance_hd/data/df_2016_10.csv")





check_variance(data=df)



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



# Feature Engineering

df["split_serial_number_3"] = df["serial_number"].str[:3]
df["split_serial_number_4"] = df["serial_number"].str[:4]
df["split_serial_number_1"] = df["serial_number"].str[:1]



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

fig =  px.histogram(data_frame=df, x="split_serial_number_4", color = "failure", nbins=100, marginal="box")
fig.show()



for c_element in list(df.columns):
    fig = px.histogram(df, x=c_element)
    fig.show()




# remove boring columns


list_of_columns_to_drop = ["date", "model", "capacity_bytes"]

df = remove_columns(df, list_columns_to_remove=list_of_columns_to_drop)

df




# serial_number encoding
list(df.columns)

cnames_serial = [i for i in df.columns if "serial" in i]
cnames_serial



dd_extra1, ohe1 = Encoder2DataFrame(data=df, column_name="split_serial_number_1")
dd_extra1.head()


dd_extra3, ohe3 = Encoder2DataFrame(data=df, column_name="split_serial_number_3")
dd_extra3.head()

dd_extra4, ohe4 = Encoder2DataFrame(data=df, column_name="split_serial_number_4")
dd_extra4.head()




# new df

df = pd.concat([df, dd_extra1, dd_extra3, dd_extra4], axis=1)
df




# remove  

list_of_columns_to_drop = ['serial_number', 'split_serial_number_3', 'split_serial_number_4', 'split_serial_number_1']

df = remove_columns(data=df, list_columns_to_remove=list_of_columns_to_drop)


df.head()




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
key = "AdaC"
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








