
import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from sklearn.preprocessing import (
    OneHotEncoder
)



def split_target_and_feature(data, target):
    data_target = data[target]
    data_features = data.drop(target, axis=1)

    target_name = target
    feature_names = list(data_features.columns)

    return data_target, data_features, target_name, feature_names



def reset_index_train_test_split(feature_data, target_data, test_size=0.2, random_state=2022):
    features_train, features_test, target_train, target_test = train_test_split(feature_data, target_data, test_size=test_size, random_state=random_state)

    features_train = features_train.reset_index(drop = True)
    features_test = features_test.reset_index(drop = True)
    target_train = target_train.reset_index(drop = True)
    target_test = target_test.reset_index(drop = True)

    return features_train, features_test, target_train, target_test


def scale_data(train, test, scaler=None):
    if scaler is None:
        scaler = MinMaxScaler()
    if len(train.shape) == 1 and len(test.shape)==1:
        train = train.to_numpy()
        test = test.to_numpy()
        train_np = train.reshape(-1,1)
        test_np = test.reshape(-1,1)
    elif len(train.shape) == 2 and len(test.shape) == 2:
        train_np = train
        test_np = test
    else:
        print("different shape of train and test")
    train_np = scaler.fit_transform(train_np)
    test_np = scaler.transform(test_np)

    return train_np, test_np, scaler




def Encoder2DataFrame(data, column_name):
    ohe = OneHotEncoder()
    transformed = ohe.fit_transform(data[[column_name]])
    cats = ohe.categories_
    cats = [i for i in cats[0]]

    dd_extra = pd.DataFrame(data=transformed.toarray(), columns=cats)
    return dd_extra, ohe


