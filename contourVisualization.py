import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

df = pd.read_csv("./Datasets/Synthesized datasets/analysis_county_data.csv")

rentSize = 10
rentSplits = np.linspace(min(df["Rent50_0"]), max(df["Rent50_0"])+1, rentSize)
incomeSize = 10
incomeSplits = np.linspace(min(df["Median household income"]), max(df["Median household income"])+1, incomeSize)
incomeSplits = [round(x) for x in incomeSplits]

matrix = np.zeros((rentSize-1, incomeSize-1))
for i in range(len(df)):
    rent = df.iloc[i]["Rent50_0"]
    income = df.iloc[i]["Median household income"]
    for j in range(1, rentSize+1):
        for k in range(1, incomeSize+1):
            if (rent >= rentSplits[j-1] and rent < rentSplits[j]) and (income >= incomeSplits[k-1] and income < incomeSplits[k]):
                matrix[j-1, k-1] += 1

matrix2 = np.zeros((rentSize-1, incomeSize-1))
for i in range(len(df)):
    rent = df.iloc[i]["Rent50_0"]
    income = df.iloc[i]["Median household income"]
    for j in range(1, rentSize+1):
        for k in range(1, incomeSize+1):
            if (rent >= rentSplits[j-1] and rent < rentSplits[j]) and (income >= incomeSplits[k-1] and income < incomeSplits[k]):
                matrix2[j-1, k-1] += df.iloc[i]["crime_rate_per_100000"]

averageCrimeRate = np.empty((rentSize-1, incomeSize-1))
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        averageCrimeRate[i, j] = 0 if matrix[i, j] == 0 else round(matrix2[i, j]/matrix[i, j], 2)

# colormap
coolwarm = cm.get_cmap('coolwarm', 256)
newcolors = coolwarm(np.linspace(0, 1, 256))
white = np.array([256/256, 256/256, 256/256, 1])
newcolors[1:20, :] = white
newcmp = ListedColormap(newcolors)

# plot it
#ms = plt.matshow(averageCrimeRate, cmap=plt.cm.Blues)
ms = plt.contourf(range(rentSize-1), range(incomeSize-1), averageCrimeRate, cmap=newcmp)
plt.colorbar(ms, label="average crime per 100000 per section")
plt.xlabel("Rent per county")
plt.xticks(range(rentSize-1), rentSplits, rotation=90)
plt.ylabel("Income")
plt.yticks(range(incomeSize-1), incomeSplits)
plt.title("Contour plot of Rent vs Income with Crime as color")
plt.show()
