
from sklearn.model_selection import KFold, cross_val_score

import pandas as pd
import numpy as np



from sklearn.preprocessing import (
    StandardScaler,
)




def model_kcross_validation_feature_importance(model, X, y, feature_columns, scoring=None, cv=10):
    feature_importances = []

    kf = KFold(n_splits=cv, shuffle=True, random_state=27)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model.fit(X_train, y_train)
        # save feature importances / weights of the model for later interpretation
        if hasattr(model, "coef_"):
            feature_importances.append(model.coef_)
        elif hasattr(model, "feature_importances_"):
            feature_importances.append(model.feature_importances_)
    # if len(y.shape) > 1:
    #     # target matrix or vector?!
    #     y_true, y_pred = np.vstack(y_true), np.vstack(y_pred)
    # else:
    #     y_true, y_pred = np.hstack(y_true), np.hstack(y_pred)
    feature_importances = np.vstack(feature_importances)
    # real cross-validated score (instead of computing it from the predicted values like when creating the plot)
    xval_scores = cross_val_score(model, X, y, scoring=scoring, cv=cv, n_jobs=-1)
    print("# cross-validated score: %.4f +/- %.4f" % (xval_scores.mean(), xval_scores.std()))

    df_feature_importance = pd.DataFrame()
    df_feature_importance["feature"] = feature_columns
    df_feature_importance["importance"] = feature_importances.mean(axis=0)
    df_feature_importance["std"] = feature_importances.std(axis=0)

    df_feature_importance = df_feature_importance.sort_values(by="importance", ascending=False)
    df_feature_importance = df_feature_importance.reset_index(drop = True)

    return df_feature_importance


def feature_importance(trained_model, df, feature_columns, target_column, digits=4, min_importance=0.0001):
    # extract X and y from dataframe
    X = df[feature_columns].to_numpy()
    y = df[target_column].to_numpy()
    if len(target_column) == 1:
        y = y.flatten()
    # scale the data (important for the linear regression models, especially to interpret the coefficients)
    X = StandardScaler().fit_transform(X)
    print("### Model:", str(trained_model))

    output_df = model_kcross_validation_feature_importance(model=trained_model, X=X, y=y, feature_columns=feature_columns, scoring=None, cv=10)

    output_df = output_df[output_df["importance"]>= min_importance]

    return output_df
