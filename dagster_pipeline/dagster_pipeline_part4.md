
# Basics to make dagster run

## Environment Variables

Within Dagster we use the Blobstorage Connector.

So we need to provide the Azure Connection String and also the Account and the Key variable.

We may also need to set the DAGSTER_HOME Variable as absolut path for dagster.


```bash

# DAGSTER_HOME = './.dagster_home'

# DAGSTER_HOME="/home/heiko/Repos/dagster/.dagster"

AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;QueueEndpoint=http://localhost:10001/devstoreaccount1"

AZURE_STORAGE_ACCOUNT="devstoreaccount1"

AZURE_ACCOUNT_KEY="Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="

```



## Dagit UI startup


Now, lets run the repository.py file on dagster.

The Dagster Daemon is for the schedulers and dagit to visualize the pipelines.

These commands should be executed in `bash`, so open two bash windows.

```bash
# execute in bash not powershell

DAGSTER_HOME=$(pwd)/.dagster dagster-daemon run

DAGSTER_HOME=$(pwd)/.dagster dagit -f ./pipelines/repository.py

```


## Dagit

### local Launchpad

On [localhost](http://localhost:3000/) we have access to the local executed dagit UI. Here we also can start a pipeline on its own or can configure the execution for a manuall run.

```bash

# Copy this to the launchpad

ops:
  load_coinbase_data:
    config:
      granularity: 15
      product_id: ETH-EUR
  upload_data_to_blob_context:
    config:
      blob_container: coinbasedata
      filename: rawdata.parquet
      subblob_container: datadownload

```


![local_execution](./assets/local_execution.png)


### Scheduler

As describted before, we use a scheduler to collect on regular basis data from the Coinbase Database.

So the scheduler should trigger the pipeline to load and save the data.

So let's have a look how this looks like.


![scheduler_execution2](./assets/scheduler_execution2.png)

Nice, but wait a second.

Why the hell, is an red pipeline present in this tutorial docu? Because i had a typo in the trigger (upload_data_to_blob instead of upload_data_to_blob_context). 


Fixed it, now its working :)


![scheduler_execution3](./assets/scheduler_execution3.png)

See, both ops are green and we see the context info as statements within the pipeline execution.

So one part of our pipeline is finished.


Let's do a bit deeper into the rabbit hole of dagster for the second part. :D


[Part5](./dagster_pipeline_part5.md)


