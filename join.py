# %%
import pandas as pd

crime = pd.read_csv("./Data/crime_data_w_population_and_crime_rate.csv")
income = pd.read_csv("./Data/2015_Median_Income_by_County.csv")
rent = pd.read_csv("./Data/filtered_FY_2016F_50_RevFinal.csv")

# %% add a dummy column for county, state to join on

# %% perform the join and remove dummy columns and duplicates??
