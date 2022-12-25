
# Data Collection for process improvement

## The Master Plan

The **Color Rating** is  visual measurement of an acceptability. 

This nominal measurement does not provide a sensitive indicator of process behavior. This is the reason we are focussing, right from the start, on *Thickness* and the 3 color measurements (L* , a* , b*) as continuos surrogates for the Color Rating.

The long-term strategy is to find a significant relationship between the color rating and the color measurement as well as a significant relationship between the continuos color measurements and process conditions.

The idea is to produce in the "optimal" process window.

## Draw backs

Yet, there are no specifiation limits for *Thickness*, *L**, *a** and *b**. 


## Action Plan:

1. Find Relationship between Color Rating and *Thickness*, *L**, *a** and *b**.

2. Specification Limits for *Thickness*, *L**, *a** and *b**.

3. Identify process conditions to produce within the specification limits of *Thickness*, *L**, *a** and *b** to produce parts that get a good color rating.


## Uncovering Relationships between Color Rating and continuos measured quality aspects

We have to replace the string classification in the dataframe by a number. (0 = normal Black)

```bash

import pandas as pd
import plotly
import plotly.express as px


data = pd.read_excel("./data/Anodize_ColorData.xlsx")

data
list(data.columns)
# ['Lot', 'Color Rating ', 'Thickness', 'L*', 'a*', 'b*']

exchange_dict = {"Normal Black": 0, "Smutty Black": 1, "Purple/Black": 2}

data["color rating dict"] = data['Color Rating '] 
data["color rating dict"] = data["color rating dict"].replace(exchange_dict)

data["color rating dict"] = [int(element) for element in data["color rating dict"]]

fig = None

fig = px.parallel_coordinates(
    data, 
    color="color rating dict",
    dimensions=['color rating dict', 'Thickness', 'L*', 'a*', "b*"],
    # color_continuous_scale=px.colors.diverging.Tealrose
)

plotly.offline.plot(fig)

```

![Overall_Correlation](./assets/Overall_correlation.png)

It is also easy to set the specification limits to almost obtain classification level 0 (Normal Black). If you make the plotly graphic you can interact with it in the internet browser to play with the limits.

![Overall_Limits](./assets/Overall_Spezification.png)


### Specifications

Using the information from the parallel coordinate plot, we can see that the four Ys should be in a specific range to produce acceptable *normal black* parts. 

I would assume the specification limits like this, to have good normal black parts. How would you set the limits?!

```bash

| Variable   | Target | Spez. Range |     Range    |
----------------------------------------------------
| Thickness  |  0.85  |    0.15     |   1.0 - 0.7  |
|    L*      |  9.75  |    1.75     |  11.5 - 8.0  |
|    a*      |  1.5   |    1.5      |   3.0 - 0.0  |
|    b*      |  0.0   |    1.5      |   1.5 - -1.5 |
----------------------------------------------------

```




[Part4](./Readme_part4.md)






