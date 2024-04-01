# importing libraries
import pandas as pd
from util import generateFrequentItemSets,generateStrongRules, colored

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

# generate the largest frequent itemsets
frequentItemsets, history = generateFrequentItemSets(data, transactionsCount*min_support)
print()
print("Frequent itemsets:")
print(colored(0, 255, 0,frequentItemsets))

strongRules = generateStrongRules(frequentItemsets,history,min_confidence)
print()
print("StrongRules:")

for rule in strongRules:
    print(colored(255, 0, 0,rule))