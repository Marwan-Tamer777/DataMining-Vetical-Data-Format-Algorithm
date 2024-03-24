# importing libraries
import pandas as pd
import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt



# load data 
OriginData = pd.read_csv("Bakery.csv",usecols = ["TransactionNo", "Items"])

# Get sample size, min support and confidence from use
sample_size = float(input("Enter sample_size as fraction: "))
min_support = float(input("Enter min_support: "))
min_confidence = float(input("Enter min_confidence: "))

# Groupby transactions into a new datafame and sample a fraction of them
transactionsData = OriginData.groupby(["TransactionNo"]).agg(list).reset_index()
transactionsDataSample = transactionsData.sample(frac=sample_size).sort_index()
transactionsCount = len(transactionsDataSample)
print("Transaction Count:", transactionsCount)
print("Min Support:", min_support*transactionsCount)

# filter items based on the sample transactions and groupby items
data = OriginData.loc[OriginData["TransactionNo"].isin(transactionsDataSample["TransactionNo"])]
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
    if(length< transactionsCount*min_support):
        data.drop(index,inplace=True)

# create candidate itemset copy then intersect the itemsets and delete the set
# smaller than min_support and output the result into the result itemsets
# Intersect the 2 n-itemsets to create n+1itemset until the resulting set is unsatisfactory
dataC = data.copy(deep = True)
history = [dataC]
frequentItemsets = []
flag = 0

while(flag !=1):
    currentItemSets = []
    dataR = pd.DataFrame(columns=data.columns)

    for index1, row1 in dataC.iterrows():
        for index2, row2 in dataC.iterrows():
            newItemSet = list(set(row1["Items"]) | set(row2["Items"]))
            if newItemSet not in currentItemSets and len(newItemSet) == (len(row1["Items"])+1):
                currentItemSets.insert(len(currentItemSets),newItemSet)
                newtransactions = list(set(row1["TransactionNo"]) & set(row2["TransactionNo"]))
                newRow = {"Items":newItemSet, "TransactionNo":newtransactions, "Frequency": len(newtransactions)}
                dataR.loc[-1] = newRow
                dataR.index = dataR.index + 1
                dataR = dataR.sort_index()
        
    # filter out itemsets that are smaller than the min_support
    for index, row in dataR.iterrows():
        if(row['Frequency']< transactionsCount*min_support):
            dataR.drop(index,inplace=True)

    # Copy the resulting set to start a new iteration
    dataC= dataR.copy(deep = True)

    # Check the generated N+1 Filtered itemsets, if it only contains one or zero itemsets stop generating
    if(len(dataR) == 0):
        frequentItemsets = history[-1][["Items","Frequency"]]
        flag = 1

    if(len(dataR) == 1):
        history.insert(len(history),dataR)
        frequentItemsets = dataR[["Items","Frequency"]]
        flag = 1

    #Append the new set into history if not empty
    if(len(dataR) >1):
        history.insert(len(history),dataR)


# # Find all subsets of size k  
# subsets = list(itertools.combinations(s, k))
        
# # Remove a subset from an item set
#  a= list(set(a) - set(b))
        
for index, row in frequentItemsets.iterrows():
    # EX: itemset = {coffee, cat , bat}
    itemSet = row["Items"]
    setSize = len(row["Items"])
    for x in range(1,setSize):
        subsets = list(itertools.combinations(itemSet, x))
        for subset in subsets:
            # EX: subset = {coffee, bat} as x = 2
            ruleSubset = list(set(itemSet) - set(subset))
            # EX: ruleSubset = {cat}


print(frequentItemsets)
print(data)
