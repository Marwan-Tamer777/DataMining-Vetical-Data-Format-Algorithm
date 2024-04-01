import pandas as pd
import itertools

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def generateFrequentItemSets(data, minFreq):
    
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
            if(row['Frequency']< minFreq):
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
        
    return frequentItemsets, history



def generateStrongRules(frequentItemsets,history,min_confidence):
    strongRules =[]
    for index, row in frequentItemsets.iterrows():
        # EX: itemset = {coffee, cat , bat}
        itemSet = row["Items"]
        itemSetFreq = row["Frequency"]
        setSize = len(row["Items"])
        for x in range(1,setSize):
            # Find all subsets of size k
            subsets = list(itertools.combinations(itemSet, x))
            for subset in subsets:
                # EX: subset = {coffee, bat} as x = 2
                # Remove a subset from an item set
                ruleSubset = list(set(itemSet) - set(subset))
                # EX: ruleSubset = {cat}

                for indexH,rowH in history[x-1].iterrows():
                    if(rowH["Items"] == list(subset)):
                        subsetFreq = rowH["Frequency"]
                
                if(itemSetFreq/subsetFreq>=min_confidence):
                    rule = str(subset)+ " --> " + "".join(ruleSubset) + ": " + str(itemSetFreq/subsetFreq)
                    strongRules.append(rule)
                    # print("STRONG RULE", subset, "-->", ruleSubset , ". ", itemSetFreq/subsetFreq)
    return strongRules