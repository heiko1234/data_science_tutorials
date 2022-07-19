
# Coinbase API

Ok, let's start with requesting information from Coinbase.

We make a minimum of imports

```bash

import pandas as pd
import numpy as np

from requests import get
import time
```




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



[Part3](./dagster_pipeline_part3.md)