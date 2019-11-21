import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("./Datasets/Synthesized datasets/analysis_county_data.csv")

rentSplits = 10
incomeSplits = 10

hist, edges = np.histogram(df["Rent50_0"], rentSplits)
hist2, edges2 = np.histogram(df["Median household income"], incomeSplits)
edges = [round(x, 2) for x in edges]
edges2 = [round(x, 2) for x in edges2]

matrix = np.zeros((rentSplits, incomeSplits))
for i in range(len(df)):
    rent = df.iloc[i]["Rent50_0"]
    income = df.iloc[i]["Median household income"]
    for j in range(1, rentSplits):
        for k in range(1, incomeSplits):
            if (rent >= edges[j-1] and rent < edges[j]) and (income >= edges2[k-1] and income < edges2[k]):
                matrix[j, k] += 1

matrix2 = np.zeros((rentSplits, incomeSplits))
for i in range(len(df)):
    rent = df.iloc[i]["Rent50_0"]
    income = df.iloc[i]["Median household income"]
    for j in range(1, rentSplits):
        for k in range(1, incomeSplits):
            if (rent >= edges[j-1] and rent < edges[j]) and (income >= edges2[k-1] and income < edges2[k]):
                matrix2[j, k] += df.iloc[i]["crime_rate_per_100000"]

averageCrimeRate = np.empty((rentSplits, incomeSplits))
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        averageCrimeRate[i, j] = 0 if matrix[i, j] == 0 else round(matrix2[i, j]/matrix[i, j], 2)

# plot it
ms = plt.matshow(averageCrimeRate, cmap=plt.cm.Blues)
plt.colorbar(ms, label="average crime per 100000 per section")
plt.xlabel("Rent per county")
plt.xticks(range(rentSplits), edges, rotation=90)
plt.ylabel("Income")
plt.yticks(range(incomeSplits), edges2)
#plt.title("Crime psuedo heatmap")
plt.show()
