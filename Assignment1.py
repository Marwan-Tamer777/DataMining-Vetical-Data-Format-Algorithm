# importing libraries
import pandas as pd
import numpy as np
from efficient_apriori import apriori

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# a) load data 
data = pd.read_csv("Bakery.csv",usecols = ["TransactionNo", "Items"])

# b) Group each transaction items into 1 row
# and get transaction count
TransactionsData = data.groupby(["TransactionNo"]).agg(list).reset_index()

TransactionsCount = data["TransactionNo"].max()

data = data.groupby(["Items"]).agg(list).reset_index()


# d) Get min support and confidence from use
min_support = float(input("Enter min_support: "))
min_confidence = float(input("Enter min_confidence: "))
print("DATA: ", min_support)

data.insert(2, "Frequency", True)
# e) delete any item that occurred less than the min support
for index, row in data.iterrows():
    length = len(row['TransactionNo'])
    data.loc[index,'Frequency'] = length
    if(length< TransactionsCount*min_support):
        data.drop(index,inplace=True)
print(data) 

dataC1 = data.copy(deep = True)
dataC2 = data.copy(deep = True)

new_df_with_col_names = pd.DataFrame(columns=data.columns)
print(new_df_with_col_names)
# for index1, row1 in dataC1.iterrows():
#     for index2, row2 in dataC2.iterrows():
