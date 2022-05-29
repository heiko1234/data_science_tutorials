
# MLFlow Part 5

# How to work with MLFlow

Now we try some experimental things that you find in [experimental](https://github.com/heiko1234/SKlearn_to_MLFLow/tree/main/experimental) within the `SKLEARN_TO_MLFLOW`. 


![MLFlow_usage](./assets/MLFlow_usage.png)


## Dumping a Model to a local folder

In the Repo SKLearn_to_MLFlow there is a folder `how_to_dump_MLFLOW_models` with two files in it:

- dump_mlflow_model.py
- dump_mlflow_model_config.yaml

In the `dump_mlflow_model_config.yaml` you need to change your local path. All models that are in the model_list: `sklearntomlflow` and others will be donloaded from the local MLFlow Docker container into your local folder.

Please ensure the folder is created **before** you download the model into it.

```bash
# in yaml

local_path: "/home/heiko/Repos/SKlearn_to_MLFLow/model_dump"

model_list: 
  - "chemical_model"
  # - "MFI_polymer"
  # - "CI_polymer"

```

To download the artifacts we need to execute the `dump_mlflow_model.py`. Change to the `how_to_dump_MLFlow_models` folder and execute the script.

```dash

# make sure to activate the .env to have all packages available

python dump_mlflow_model.py
```

Here you can see how the execution works.

![execute_model_dumping](./assets/execute_model_dumping.png)


As a result to this execution the `sklearntomlflow` folder is created with all artifacts in it. The second model is part of the `SKLearn_to_MLFlow` Repo and contains only some additional .json files.

![result_dump](./assets/result_model_dump.png)


## Feature Limit Dict



## Feature dtype Dict


## Prepare some data


## Model Predictions


# Conclusion



