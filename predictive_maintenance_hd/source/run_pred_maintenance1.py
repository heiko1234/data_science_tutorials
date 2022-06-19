





import pandas as pd



from predictive_maintenance_hd.source.data_utility import (
    Encoder2DataFrame,
    remove_columns,
    check_variance
)


# for df data 

target_name   #failure
feature_names   # all feature names relevant






# load data

# 7 days in advanced
df = pd.read_csv("./predictive_maintenance_hd/data/df_2017_7.csv")






# Feature Engineering

df["split_serial_number_3"] = df["serial_number"].str[:3]
df["split_serial_number_4"] = df["serial_number"].str[:4]
df["split_serial_number_1"] = df["serial_number"].str[:1]




dd_extra1, ohe1 = Encoder2DataFrame(data=df, column_name="split_serial_number_1")
dd_extra1.head()


dd_extra3, ohe3 = Encoder2DataFrame(data=df, column_name="split_serial_number_3")
dd_extra3.head()

dd_extra4, ohe4 = Encoder2DataFrame(data=df, column_name="split_serial_number_4")
dd_extra4.head()




# new df

df = pd.concat([df, dd_extra1, dd_extra3, dd_extra4], axis=1)
df

list(df.columns)



# remove  

list_of_columns_to_drop = ['serial_number', 'split_serial_number_3', 'split_serial_number_4', 'split_serial_number_1']

df = remove_columns(data=df, list_columns_to_remove=list_of_columns_to_drop)





# for df_merged_10 data for 2017
df = df.loc[:, feature_names+[target_name]]
df


# feautre names from different script
feature_data = df.loc[:, feature_names]


test_data = df.loc[:, "failure"]


# 

# Data Preprocessing


# take scaler from pred_maintenance or pred_maintenance2 


scaled_feature_data=scaler.transform(feature_data) 
scaled_feature_data



from sklearn.metrics import balanced_accuracy_score


output_df = pd.DataFrame(columns=["model_name", "r2_test", "bas_test"])
output_df




r2_test=clf.score(scaled_feature_data, test_data) 
r2_test


bas_test=balanced_accuracy_score(test_data, clf.predict(scaled_feature_data)) 
bas_test


dict = {"model_name": key,
    "r2_test": r2_test,
    "bas_test": bas_test
}

output_df = output_df.append(dict, ignore_index = True)
output_df


