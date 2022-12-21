
# Collecting Data

## Graph Data

Since the process is complex enough, we will have a closer look into graph organized data structures.

![graph_data](./assets/Data_sensor_structure.png)

Maybe we will try to fetch data from Microsoft Kusto via Graph based main process view.



## Quality Parameters

there are four continous CTQs for the anodizing process: 
anodized coating thickness and the treee color coordinates. 

## Critical to Qualit (CTQ)

There are 4 continuous measured quality aspects:

- coating thickness
- 3 clor coordinates

These things are measured with 3 different measurement systems:

- backscatter gauge
- spectrophotometer
- vsiual color inspction rating that classifies parts as good or bad


### CIELAB

![cielab](./assets/cielab_colorspace.png)

*L** is a measure of lightness of the color (the range is 0 - 100), with lower values indicating darker color

*a** is a measure of red/green. Positiv values indicate redness and negative values indicate greeness.

*b** is a measure of yellow/blue. Positiv values indicate yellowness and negative values indicate blueness.


### MSA Backscatter Gauge

The Backscatter Gauge is to measure thickness.

1 Gauge is used but up to 12 operators may measure.


The MSA is preformed with:
- 1 gauge
- 3 random operators (out of 12)
- 5 random parts (which are measured twice)

This will be done with a DOE Full Factorial Design. The study will be performed in a complete random order.

We will make a Multi-Vari plot.

[Here](./source/multi_vari.py) are the basic plot functions, while [here](./source/usage_multi_vari.py) is the usage of the functions.


```bash 

# Here very simple function usage

import pandas as pd

from rusted_parts.source.multi_vari import (
    make_muti_vari_plot,
    multi_vari_plot
)

data = pd.read_excel("./rusted_parts/data/Thickness_MSA.xlsx")

make_muti_vari_plot(
    data=thickness_data,
    operator="Operator",
    part="Part",
    parameter="Thickness",
    )

```



This are the data of the MSA:

![data_gauge](./assets/data_msa_gauge.png)

The chart for *Thickness* shows for each Operator and Part, the two measurements obtained by that Operator.

![multi_vari_gauge](./assets/multi_vari_plot1.png)


Since there are several values for each Operator and Part, we can calculate the standard deviation. 

![multi_vari_gauge3](./assets/multi_vari_plot3.png)

Regarding the average values for each Operator and Part, we see the wide range from about 0.22 (Carl, Part 4) to around 2.00 (Lisa, Part 3).
![multi_vari_gauge2](./assets/multi_vari_plot2.png)

In a MSA, the focus is on the variation inherrent in the measurement process itself rather than on studying part-to-part variation.


### Improvement of *Thickness* Measurement

Back to the *Thickness* measurement the accuracy should be at least 0.1, since it need to be measured between 0.0 and 1.6 .


- Measuements on the same Part made by the sampe Operator can differ by 0.2 - 0.45.

- Different Operators differ in their overall measurement of the parts, see the average values for all parts for the different operators.

- There are differential effects in how some operators measure some parts. In other words: there is an **Operator by Part** interaction. See Part 2, which is measured high by Scott and low by Lisa.


To interprete these data we will also use an gage r&r (six sigma approach): 

```bash
                                repeatabilit
                                |
                    gage r & r--|               operator
                    |           |               |
total variability --|           reproduibility--|
                    |                           |
                    part-to-part                interaction

```

When using the [Gage_RnR](./source/Gage_RandR.py) we can generate the graphics but also this table [usage_gage_rnr](./source/usage_gage_randr.py): 

```bash

                    names  variations  percent of total
0                Gage R&R    0.089643            50.576
1           Repeatability    0.050163            28.302
2         Reproducibility    0.039480            22.274
3   Interaction Variation    0.019591            11.053
4  part-to-part Variation    0.068010            38.371
5         Total Variation    0.177244           100.000

```

**Repeatablity**: Repeated easurements of the same part by the same operator with the same instruments

**Reproducability**: Repeated measurements of the same part by different operators using different instruments

**part-to-part Variation**: Differences in the parts used in the MSA: here parts are represented by batches

**Interaction Variation**: Differences due to the interaction components. Here the interaction components are *Operator x Instrument*, *Operator x Batch* and *Instrument x Batch*.

It can be seen that the Gage R&R component is very large compared to the product variation (part-to-part) variance. This suggests that the measurement system has difficuty distinguishing batches.
A control chart monitoring this process is mainly monitoring measurement variation. 

The *Batch* variation accounts is ca. 40% of the total variation.

Recalling that the measurement system range, measured as six standard deviations should take up at most 10 % of the tolerance range, which is 10 % x (1.6 - 0.0) = 0.16 units.

The standard deviation of the measurement system is about (0.0896 / 2) x 6 = 0.268 units which is much higher than the expected 0.16 units.



### Difficulties when measuring a sample

The 3 Operators checked each other when performing the measurement and found:

- diffculty in repeating the exact positioning of parts 

- gauge proves to be sensitive to the positioning 

- amount of pressure appllied to the gauge head on the part affet the thickness measurement

- operators do not calibrate the gauge in the same manner, which lead to reproducibility variations



### Measurement improvements

The metrology department and a few operators worked together to design a fixture that 

- automatically locates the gauge on the part

- adjust the pressure of the gauge head on the part

- the team define and implement a standard for calibration practice.



According to these changes a new measurement with the operators with 5 new parts is performed
[Here](./data/Thickness_MSA_2.xlsx) are the data.


![multi_vari_plot_msa2](./assets/multi_vari_plot_msa2.png)

Now, we also can overlay the plots: 

![multi_vari_overlay](./assets/multi_vari_overlay.png)


We also get these values out of the Gage R&R: 

The Gage R&R value of 0.0000024 (= 0.024 * 10^-3 units = 0.012 * 10^-3 sigma) which seems to be more sufficient than 0.089 as we have seen before. 

```bash

                    names    variations  percent of total
0                Gage R&R  2.416667e-06             0.003
1           Repeatability  5.333333e-07             0.001
2         Reproducibility  1.883333e-06             0.002
3   Interaction Variation  1.666667e-06             0.002
4  part-to-part Variation  7.994006e-02            99.995
5         Total Variation  7.994414e-02           100.000

```

This indicates that the measurement system will easily distinguish parts that differ by 0.1 thousandths. 

Now, the *Thickness* measurement process is extremely capablet.


### MSA Visual Color Rating

At this point, we focus on the improvement of the manual color rating.
Different root-causes produce different bad colors.

```bash

                color rating
                    |
            ------------------
            |                |
           good             bad
            |                |
        normal black     -----------------
                        |                 |
                    purple black     smutty black

```

There are 8 different inspectors involved in the inspectio, 3 are randomly choosen.
50 random parts from production are taken, with minimum of 12 each of *normal black*, *purple black* and *smutty black*


To prove that the inspectors have labeled the parts correctly, an expert is choosen to make the final classification.


For this MSA the consensus of classification of 2 inspectors will be considered correct and will be used to evaluate the accuracy of the inspectors.

We choose: Hal, Carly and Jake as inspectors (3 out of 8)

Each part is inspected twice.


## Kappa or the Agreement Comparison

First we will focus on the kappa criterion in the agreement comparison.
A Kappa value of > 0.80 reflects almost perfect agreement, while a kappa of 0.60 - 0.80 indicates substantial agreement.

We calculate the inter rater comparison with [this](./source/usage_agreement.py)

```bash
list_of_raters= ["Hal", "Carly", "Jake"]

inter_rating(data=data, list_of_rater=list_of_raters)


  rater1 rater2   kappa
0    Hal  Carly  0.7265
1    Hal   Jake  0.7274
2  Carly   Jake  0.8184
```


and also the comparison with the external standard (external expert):

```bash
expert_rating(data = data, list_of_rater=list_of_raters, expert="Expert Rating")


  rater1         expert   kappa
0    Hal  Expert Rating  0.8023
1  Carly  Expert Rating  0.8635
2   Jake  Expert Rating  0.9242
```

We also calculate the misclassifications of all test raters to the external standard: 

```bash
misclassifications(data=data, list_of_rater=list_of_raters, expert="Expert Rating", part="Part")


  Normal Rating  Normal Black  Purple/Black  Smutty Black
0  Normal Black           NaN           7.0           7.0
1  Purple/Black           8.0           NaN           1.0
2  Smutty Black           4.0           NaN           NaN
```

We have room for improvements, as Hal has and Carly are blow 90% compared to the expert and there are several missmatches compared to the expert rating.



## Data Collection















[Part3](./Readme_part3.md)


