
# Basics of Dagster

## Structure of repo

Let's start with the structure.

```bash

|
|- pipelines
    |- general
        |- utility.py
        |- resources.py
    |- job_blablabla
        |- op.py
        |- graph.py
        |- job.py
        |- trigger.py
|
|- repository.py
|- .env
|- .gitignore
|- poetry.loc
|- poetry.toml
|- pyproject.toml

```

In *general* i like to store `utility` and `resource` functions.

In *pipelines* we can have several `job` folders that contain usually `op.py`, `graph.py`, `job.py` and a `trigger.py`.

Outside of the `pipelines` folder we need a `repository.py` file.

Moreover we need a few standard things like `.env`, `poetry files` and a `.gitignore` file.


## Ops

We need 2 ops: 

- load_coinbase_data
- upload_data_to_blob_context

First, we load the data from coinbase and upload these data to blob.

We will parse some information from the sensor to the ops and therefore we have no inputs.

We can monitore some of our passed informations via context.log (`context.log.info(f"product_id: {product_id}")`)

```bash

from dagster import op
from pathlib import Path
import os
import pandas as pd


from pipelines.job_fetch_coinbase_data.coinbase_functions import (
    public_candles
)
from pipelines.general.resources import (
    BlobStorageConnector,
    upload_data_to_blob
)


@op()
def load_coinbase_data(context):

    product_id = context.op_config["product_id"]
    granularity = context.op_config["granularity"]

    context.log.info(f"product_id: {product_id}")
    context.log.info(f"granularity: {granularity}")

    data = public_candles(product_id=product_id, start=None, end= None, granularity=granularity, localtime=True)

    context.log.info(f"data: {data.head()}")

    return data

```

To upload our resulted small dataframe we use the `BlobStorageConnector` or better the `upload_data_to_blob` functions.

We need to pass the blobcontainer, subblobcontainer and the filename to upload the df to the blobstorage (on azurite).


```bash

@op()
def upload_data_to_blob_context(context, df):

    containername = context.op_config["blob_container"]
    context.log.info(f"containername: {containername}")

    subcontainername = context.op_config["subblob_container"]
    context.log.info(f"subcontainername: {subcontainername}")

    filename = context.op_config["filename"]
    context.log.info(f"filename: {filename}")

    file_name = filename.split(".")[0]
    file_type = filename.split(".")[1]

    context.log.info(f"file_name: {file_name}")
    context.log.info(f"file_type: {file_type}")

    upload_data_to_blob(df=df, 
        container_name=containername, 
        subcontainer_name=subcontainername, 
        filename=file_name, 
        filetype=file_type)

```

## Graph

In the graph file we load and arrange the loaded functions.

It looks simple and easy.


```bash

from dagster import graph

from pipelines.job_fetch_coinbase_data.ops import (
    load_coinbase_data,
    upload_data_to_blob_context
)


@graph
def coinbase_data_execution_graph():

    df = load_coinbase_data()

    upload_data_to_blob_context(df=df)


```

## Job

The job file is also very simple. We load the graph function and transform the graph function to a job.

We can give at a name, which will be displayed later on.

We can give it some resources, but so far it is fine to leave them.


```bash

from pipelines.job_fetch_coinbase_data.graph import (
    coinbase_data_execution_graph
)


job_fetch_coinbase_data = coinbase_data_execution_graph.to_job(
    name="coinbase_data_fetch",
    resource_defs={}
)

```

## Trigger

A Trigger could be a scheduler or a sensor (if the pipeline should be triggered when the data are changing over time).

Here we use a scheduler which is more or less a cron job implementation.

We load our job and give some information to the scheduler decorator.

The scheduler decorator contain the job name, when it should be executed (like a cron job) and the pipeline name.

The scheduler function is very easiy, we only give the information to the context of the ops that we need for execution.


```bash

from dagster import ScheduleEvaluationContext, schedule

from pipelines.job_fetch_coinbase_data.job import (
    job_fetch_coinbase_data
)

@schedule(
    job=job_fetch_coinbase_data,
    cron_schedule="*/2 * * * *",  # every 2 min
    pipeline_name="schedule_coinbase_data"
)
def trigger_fetch_coinbase_data_execution(context: ScheduleEvaluationContext):
    output = {
        "ops":
            {
                "load_coinbase_data":
                    {"config": 
                        {
                            "product_id": "ETH-EUR",
                            "granularity": 15
                        }
                    },
                "upload_data_to_blob":
                    {"config":
                        {
                            "blob_container": "coinbasedata",
                            "subblob_container": "datadownload",
                            "filename": "rawdata.parquet"
                        }
                    }
            }
    }
    return output

```


## Repository

The repository file we late on into dagit (dagster UI). 

Everything that should be executed or at least loaded into dagit we should load in this file. 

In this case we load the job and its trigger (scheduler) into the repository file.


```bash

from dagster import repository

from pipelines.job_fetch_coinbase_data.job import (
    job_fetch_coinbase_data
)
from pipelines.job_fetch_coinbase_data.trigger import (
    trigger_fetch_coinbase_data_execution
)


@repository
def data_pipeline():
    """Dagster repository to run pipelines for project"""


    return [
        job_fetch_coinbase_data,
        trigger_fetch_coinbase_data_execution
    ]

```




[Part4](./dagster_pipeline_part4.md)
