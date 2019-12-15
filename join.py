# %%
import pandas as pd

crime = pd.read_csv("./Datasets/Original datasets/crime_data_w_population_and_crime_rate.csv")
print(len(crime))
income = pd.read_csv("./Datasets/Original datasets/median_income.csv")
print(len(income))
rent = pd.read_csv("./Datasets/Synthesized datasets/filtered_FY_2016F_50_RevFinal.csv")
print(len(rent))

# %% add a dummy column for county, state to join on
incomeJoin = pd.Series( [income.iloc[i]["County"] + ", "+income.iloc[i]["State Code"] for i in range(len(income))] )
income = pd.concat((income, incomeJoin.rename("incomeJoin")), axis=1)
rentJoin = pd.Series( [rent.iloc[i]["countyname"] + ", "+rent.iloc[i]["state_alpha"] for i in range(len(rent))] )
rent = pd.concat((rent, rentJoin.rename("rentJoin")), axis=1)

# %% perform the join and remove the dummy columns
df = crime.merge(right=rent, how="left", left_on="county_name", right_on="rentJoin")
df = df.merge(right=income, how="left", left_on="county_name", right_on="incomeJoin")
df.drop(columns=["incomeJoin", "State_x", "rentJoin"], inplace=True)
df.rename(columns={'State_y':"State"}, inplace=True)

# %% final sorting then save it
df = df[df["Rent50_0"].notnull()] #LaSalle County, IL has no rent data
df.sort_values(['state_alpha', 'countyname'], inplace=True)
df.to_csv("./Datasets/Synthesized datasets/raw_joined_county_data.csv", index=False)
