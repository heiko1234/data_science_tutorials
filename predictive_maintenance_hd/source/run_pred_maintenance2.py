





import pandas as pd



# for df data 

target_name   #failure
feature_names   # diff_smart_9_raw





# load data

# 7 days in advanced
df = pd.read_csv("./predictive_maintenance_hd/data/df_2017_7.csv")


# 10 days in advanced
df_10 = pd.read_csv("./predictive_maintenance_hd/data/df_2017_10.csv")





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

list(df.columns)



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


