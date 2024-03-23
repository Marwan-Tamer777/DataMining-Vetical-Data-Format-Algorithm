# importing libraries
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# load data 
OriginData = pd.read_csv("Bakery.csv",usecols = ["TransactionNo", "Items"])

# Get sample size, min support and confidence from use
sample_size = float(input("Enter sample_size as fraction: "))
min_support = float(input("Enter min_support: "))
min_confidence = float(input("Enter min_confidence: "))

# Groupby Transactions into a new datafame and sample a fraction of them
TransactionsData = OriginData.groupby(["TransactionNo"]).agg(list).reset_index()
TransactionsDataSample = TransactionsData.sample(frac=sample_size).sort_index()
TransactionsCount = len(TransactionsDataSample)
print(TransactionsCount)

# filter items based on the sample transactions and groupby items
data = OriginData.loc[OriginData["TransactionNo"].isin(TransactionsDataSample["TransactionNo"])]
data = data.groupby(["Items"]).agg(list).reset_index()
data.insert(2, "Frequency", True)

# delete any item that occurred less than the min support 
# and append the frequency column
# and change the 1-item itemsets to list for future processing
# and remove duplicate transactions from items that were bought multiple times 
for index, row in data.iterrows():
    itemset = [row["Items"]]
    length = len(row['TransactionNo'])
    transactions = list(dict.fromkeys(row['TransactionNo']))

    data.loc[index,'Frequency'] = length
    data.loc[index,'Items'] = itemset
    data['TransactionNo'][index] = transactions
    if(length< TransactionsCount*min_support):
        data.drop(index,inplace=True)

# create candidate itemset copy then intersect the itemsets and delete the set
# smaller than min_support and output the result into the result itemsets
dataC1 = data.copy(deep = True)
dataR = pd.DataFrame(columns=data.columns)
History = [dataC1]


# Intersect the 2 n-itemsets to create n+1itemset
# and append to history
currentItemSets = []
for index1, row1 in dataC1.iterrows():
    for index2, row2 in dataC1.iterrows():

        newItemSet = list(set(row1["Items"]) | set(row2["Items"]))
        if newItemSet not in currentItemSets and len(newItemSet) == (len(row1["Items"])+1):
            currentItemSets.insert(len(currentItemSets),newItemSet)
            newTransactions = list(set(row1["TransactionNo"]) & set(row2["TransactionNo"]))
            newRow = {"Items":newItemSet, "TransactionNo":newTransactions, "Frequency": len(newTransactions)}
            dataR.loc[-1] = newRow
            dataR.index = dataR.index + 1
            dataR = dataR.sort_index()
            History.insert(len(History),dataR)

# filter out itemsets that are smaller than the min_support
for index, row in dataR.iterrows():
    if(row['Frequency']< TransactionsCount*min_support):
        dataR.drop(index,inplace=True)

print(data)
print(dataR)