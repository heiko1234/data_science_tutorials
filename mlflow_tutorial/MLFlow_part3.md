

# MLFlow Part 3

## MLFlow Model Registry

When running the script either in a Pipeline (Azure or Dagster) or local execution, we create some artifacts.

We can have a look on the model training outcome and the models created on [local_mlflow](localhost:5000) and see our experiments listed for this.

![local_mlflow](./assets/mlflow_experiments.png)


Choose a model which seems to be sufficient from the metrics, select it.

![workflow_mlflow](./assets/mlflow_choose_model.png)

When you are in an experiment, there is a button "register model" 

![workflow_mlflow2](./assets/model_register.png)

It is worth to also have a deeper look into the artifacts that are stored, which we have created with our "sklearn_to_mlflow.py" execution. We can create and save even more artifacts.

![workflow_mlflow2](./assets/model_artifacts.png)

If we start new, there is no model name we can register the experiment to, so choose your model name. I choose "chemical_model"

![workflow_mlflow4](./assets/model_register2.png)

Now, we have in the register card "models" our first model.

![workflow_mlflow4](./assets/registered_model.png)

Now, we need to stage the registered experiement, to either "staging" or "production"

![workflow_mlflow5](./assets/model_staging.png)

If we have done it, we find our first version of the model in staging or production. Try out your self.

![workflow_mlflow5](./assets/model_staged.png)


[Part4](./MLFlow_part4.md)
