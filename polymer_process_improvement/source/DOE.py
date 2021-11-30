
# https://pypi.org/project/pyDOE2/
# https://pythonhosted.org/pyDOE/


from pyDOE2 import *
import pandas as pd
import random



seed = random.seed(42)
print(random.random()) 



# 3 batches
# 3 technicans
# 4 instruments

ff = fullfact([3, 3, 4])

df = pd.DataFrame(data = ff, columns =["batch", "technican", "instrument"])

df


# to shuffle the data frame 
df = df.sample(frac=1).reset_index(drop=True)

# replace the technicans by name
dict_technicans={0.0: "Klaus", 1.0:"Peter", 2.0: "Hans"}
df["technican"] = df["technican"].replace(dict_technicans)

# replace instruments to A, B, C, D
dict_instrument={0.0: "A", 1.0: "B", 2.0: "C", 3.0: "D"}
df["instrument"] = df["instrument"].replace(dict_instrument)


df

df.shape(36, 3)

# Do this twice with different seeds to have a repetion in your dataframe and have covered 72 experiments.

