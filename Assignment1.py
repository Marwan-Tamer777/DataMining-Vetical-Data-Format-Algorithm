# importing libraries
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# a) load data 
data = pd.read_csv("Bakery.csv",usecols = ["TransactionNo", "Items"])

# b) Group each transaction items into 1 row
# and get transaction count
TransactionsData = data.groupby(["TransactionNo"]).agg(list).reset_index()
TransactionsCount = data["TransactionNo"].max()
data = data.groupby(["Items"]).agg(list).reset_index()
data.insert(2, "Frequency", True)


# d) Get min support and confidence from use
min_support = float(input("Enter min_support: "))
min_confidence = float(input("Enter min_confidence: "))


# e) delete any item that occurred less than the min support 
# and append the frequency column
# and change the 1-item itemsets to list for future processing
for index, row in data.iterrows():
    itemset = [row["Items"]]
    length = len(row['TransactionNo'])

    data.loc[index,'Frequency'] = length
    data.loc[index,'Items'] = itemset
    if(length< TransactionsCount*min_support):
        data.drop(index,inplace=True)

# f) create 2 candidate itemsets copies to intersect and output the result into the result itemsets
dataC1 = data.copy(deep = True)
dataC2 = data.copy(deep = True)
dataR = pd.DataFrame(columns=data.columns)

# for index1, row1 in dataC1.iterrows():
#     for index2, row2 in dataC2.iterrows():
        