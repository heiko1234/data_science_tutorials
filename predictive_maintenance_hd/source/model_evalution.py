
import pandas as pd
from sklearn.metrics import balanced_accuracy_score


def model_evaluation(model_dict, train_np, test_np, target_train, target_test):

    output_df = pd.DataFrame(columns=["model_name", "r2_train", "r2_test", "bas_train", "bas_test"])
    output_df

    for key in model_dict.keys():
        model = model_dict[key]

        clf=model.fit(X= train_np, y=target_train)

        r2_train=clf.score(train_np, target_train)  
        r2_test=clf.score(test_np, target_test) 

        bas_train=balanced_accuracy_score(target_train, clf.predict(train_np)) 
        bas_test=balanced_accuracy_score(target_test, clf.predict(test_np)) 


        dict = {"model_name": key,
                "r2_train": r2_train,
                "r2_test": r2_test,
                "bas_train": bas_train,
                "bas_test": bas_test
            }

        output_df = output_df.append(dict, ignore_index = True)

    return output_df
