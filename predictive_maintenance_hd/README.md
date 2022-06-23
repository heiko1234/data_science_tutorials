# Predictive Maintenance


## Data 

The original data can be downloaded from [backblaze](https://www.backblaze.com/b2/hard-drive-test-data.html). The data from Q1/2016 - Q4/2016 are our training data. The testdata are Q2/2017.

The original data were cleaned and restructured.

* removed NaNs
* only most frequent drive models: 'ST4000DM000'
* a dataframe was created (ready-to-use)


These Data have been prepared by Franziska Horn for one of her workshops. Thank you Franz!

Here i will have a deeper look into these data to improve my prediction skills and make a better model than in your workshop. :)


I did and therefor i like to have the way to do it as a walk through tutorial.



Data to predict failures a week in advance are labeled with a suffix:

- 10 days in advanced: df_2016_10.csv
- 7 days in advanced: df_2016_7.csv
- 5 days in advanced: df_2016_5.csv

Data to evaluate the final model we take from 2017.

If you check backblaze homepage, there are more data available. Have fun to work with them.


## Goal of this tutorial

In this tutorial we will have a look into different approaches for predictive maintenance (in this case hd computer disks).

We will have a look into data preprocessing and correlations. 



## Reusability 

Functions that maybe suitable for reusage are put in separated python files. These files are:

- data_utility.py
- feature_importance.py
- graphics.py
- model_evaluation.py


[Part2](./Readme_part2.md)
