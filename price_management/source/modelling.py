


from numpy.core.fromnumeric import mean
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor


from sklearn.compose import make_column_selector as selector

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer



def translate(data, columnlist):
    for element in columnlist:
        try:
            data[element] = data[element].str.replace(",", ".")
            data[element] = pd.to_numeric(data[element], errors='coerce')
        except:
            continue
    return data







data = pd.read_csv("./price_management/data/baseline.csv")

data.columns

data = translate(data = data, columnlist = ["Price Increase"])


data

# make a selection on the inputs and outputs for the analysis
new_columns = ["Region", "Supply Demand Balance", "Sales Rep Experience", "Buyer Sophistication", "Product Category", "Price Increase"]


# working with only a subdata dataframe
subdata = data.loc[:, new_columns]
subdata

test_data = subdata.iloc[5:6,:]
test_data




# pd.get_dummies(subdata["Region"])


# https://inria.github.io/scikit-learn-mooc/python_scripts/03_categorical_pipeline_column_transformer.html


# easy selection of categoric and object columns
categorical_columns_selector = selector(dtype_include=object)
categorical_columns = categorical_columns_selector(subdata)
categorical_columns
# results in:
# ['Region', 'Supply Demand Balance', 'Sales Rep Experience', 'Buyer Sophistication', 'Product Category', 'Price Increase']



# make a ColumnTransformator for these columns
t = ColumnTransformer(transformers=[
    ('onehot', OneHotEncoder(), categorical_columns),
    # ('scale', StandardScaler(), ['col1', 'col2'])
], remainder='passthrough')


# Transform the features
features = t.fit_transform(subdata.loc[:,['Region', 'Supply Demand Balance', 'Sales Rep Experience', 'Buyer Sophistication', 'Product Category']])
result = subdata.loc[:,"Price Increase"]


poly = PolynomialFeatures(degree= 2, interaction_only=True)
features2= poly.fit_transform(features)

result

features
features2


# with polynominal Features
reg = LinearRegression()
model = reg.fit(features2, result)
reg_score = reg.score(features2, result)
reg_score  # 0.786


# with single Features
reg = LinearRegression()
model = reg.fit(features, result)
reg_score = reg.score(features, result)
reg_score  # 0.735

subdata["predict"] = model.predict(features)



randomforest = RandomForestRegressor(random_state=0, n_jobs=-1, n_estimators=150, max_features=4, bootstrap = True)

model_rf = randomforest.fit(features, result)
# yes, it needs to be flatten!

round(model_rf.score(features, result), 4)  #0.83


test_data
test_features = t.transform(test_data.loc[:,['Region', 'Supply Demand Balance', 'Sales Rep Experience', 'Buyer Sophistication', 'Product Category']])
test_features

test_result = test_data.loc[:,"Price Increase"]
test_result #6.63

test_features2= poly.transform(test_features)


model_rf.predict(test_features)[0]

model.predict(test_features)[0]

# or
model.predict(test_features2)[0]


# random forest prediction
fig = px.scatter(x=subdata["Price Increase"], y=model_rf.predict(features))
fig.show()

# linear regression prediction
fig = px.scatter(x=subdata["Price Increase"], y=subdata["predict"])
fig.show()


subdata["diff"] = subdata["Price Increase"]-subdata["predict"]


np.std(subdata["diff"])  # 1.05



# group data analysis
grouped_data = subdata.groupby(["Product Category", "Sales Rep Experience"]).mean().reset_index()

grouped_data

fig = px.line(grouped_data, x = "Product Category", y = "Price Increase", color = "Sales Rep Experience", markers=True)
fig.show()


# group data analysis, part 2
grouped_data = subdata.groupby(["Product Category", "Buyer Sophistication"]).mean().reset_index()

grouped_data

fig = px.line(grouped_data, x = "Product Category", y = "Price Increase", color = "Buyer Sophistication", markers=True)
fig.show()


