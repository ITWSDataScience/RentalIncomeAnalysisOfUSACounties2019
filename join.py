# %%
import pandas as pd

crime = pd.read_csv("./Data/crime_data_w_population_and_crime_rate.csv")
income = pd.read_csv("./Data/2015_Median_Income_by_County.csv")
rent = pd.read_csv("./Data/filtered_FY_2016F_50_RevFinal.csv")

# %% add a dummy column for county, state to join on
incomeJoin = pd.Series( [income.iloc[i]["County"] + ", "+income.iloc[i]["State Code"] for i in range(len(income))] )
income = pd.concat((income, incomeJoin.rename("incomeJoin")), axis=1)
print(income.head())

# %% perform the join and remove the dummy columns
df = crime.merge(right=rent, how="left", left_on="county_name", right_on="areaname")
df = df.merge(right=income, how="left", left_on="county_name", right_on="incomeJoin")
df.drop(columns=["incomeJoin"], inplace=True)

# %% save it
df.sort_values(['state_alpha', 'countyname'], inplace=True)
df.to_csv("./Data/raw_joined_county_data.csv", index=False)
