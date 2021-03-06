
# Coinbase API

Ok, let's start with requesting information from Coinbase.

We make a minimum of imports

```bash

import pandas as pd
import numpy as np

from requests import get
import time
```

[Here](https://docs.cloud.coinbase.com/exchange/docs) we can find the API documentation.

Don't worry, we only like to get the information from the exchange, which should be easy.

We like to get the candle information and therefor have the query endpoint `"http://api.exchange.coinbase.com/products/{product_id}/candles"`
for different product_id like `ETH-EUR`.

So lets split this endpoint and make a small parse function for a more generic approach.

When we get a 200 response, we have a success and need to make a dataframe out of it.



```bash
def parse_response(path):

    # query_endpoint = "https://api.pro.coinbase.com"
    query_endpoint = "https://api.exchange.coinbase.com"

    new_query_endpoint = query_endpoint+path

    headers = {
        "Accept": "application/json",
    }

    response = get(
        new_query_endpoint,
        headers=headers,
        proxies=False,
        params=None, 
        verify=False, 
    )

    if response.status_code == 200:
        print("get call successful")
        return response
    else:
        print("an error happend")
        return response

```


Ok, since we splitted the functionality to a response parsing function and a decoding function of the response, we need to have 
a deeper look into the decoding function.

We get a json back as response that we need to form to a dataframe, we also need to give it some column names.

Moreover, we need to transform the time column, since it is UTC but we like to have it a local time zone.



```bash

def public_candles(product_id="ETH-EUR", start=None, end= None, granularity=None, localtime=True):

    product_id = product_id.upper()

    req_url = (f"/products/{product_id}/candles")

    granularity = granularity*60  # to be in min

    url_extension = "?"

    if granularity is not None:
        url_extension = f"{url_extension}granularity={granularity}"

    if start is not None:
        url_extension = f"{url_extension}&start={start}"
        
    if end is not None:
        url_extension = f"{url_extension}&end={end}"
    
    if (granularity is None) and (start is None) and (end is None): 
        url_extension = ""
    
    req_url = req_url+url_extension

    response = parse_response(
        path=req_url,
    )

    if response.status_code == 200:
        content = response.json()
        df =pd.DataFrame(data = content, columns=["time", "low", "high", "open", "close", "volume"])

    else: 
        df =pd.DataFrame(columns=["time", "low", "high", "open", "close", "volume"])

    try:
        if localtime:
            df["time"] = [time.strftime("%Y-%m-%d %H:%M", time.localtime(df["time"][i])) for i in range(df.shape[0])]
        else:
            df["time"] = [time.strftime("%Y-%m-%d %H:%M", time.gmtime(df["time"][i])) for i in range(df.shape[0])]
    except BaseException:
        df =pd.DataFrame(columns=["time", "low", "high", "open", "close", "volume"])

    df = df.sort_values(by="time", ascending=True)
    df = df.reset_index(drop = True)

    return df

```


Ok, both functions are very simple and we should not concentrate to much on them since we like to do something with dagster :)




[Part3](./dagster_pipeline_part3.md)