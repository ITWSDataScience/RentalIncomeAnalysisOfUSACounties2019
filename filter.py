# %%
import pandas as pd
pd.options.mode.chained_assignment = None

rawRent = pd.read_csv("./Data/FY2016F_50_RevFinal.csv")
countyNames = rawRent["countyname"]
lastState = countyNames[countyNames == "Weston County"].index[0]
rawRent = rawRent.iloc[:lastState+1]


# %% get the properly reported
grouped = rawRent.groupby(["countyname", "state_alpha"])

indices = []
for key in grouped.groups.keys():
    # properly reported, append to the dataframe
    if len(grouped.groups[key]) == 1:
        indices.append(grouped.groups[key][0])
filteredRent = rawRent.iloc[indices]

# %% Get the improperly reported
populationSums = grouped["pop2010"].sum()
for key in grouped.groups.keys():
    if len(grouped.groups[key]) > 1:

        # adjust the row to be added
        # the fips can't be determined but set county details to defaults
        row = rawRent.iloc[grouped.groups[key][0]]
        row["fips2000"] = None
        row["fips2010"] = None
        row["county_town_name"] = row["countyname"]
        row["CouSub"] = 99999

        # Get each stddev of rend reported
        for rentTier in ["Rent50_2", "Rent50_0", "Rent50_1", "Rent50_3" ,"Rent50_4"]:
            rent = 0
            # Degenerate (assuming there is no county with actually different town rents meeting this)
            if rawRent.iloc[grouped.groups[key][0]][rentTier] == rawRent.iloc[grouped.groups[key][1]][rentTier]:
                rent = rawRent.iloc[grouped.groups[key][0]][rentTier]
            # Weighted sum
            else:
                for index in grouped.groups[key]:
                    if rawRent.iloc[index]["pop2010"] > 1 and pd.notna(rawRent.iloc[index]["pop2010"]):
                        rent += rawRent.iloc[index][rentTier] * rawRent.iloc[index][rentTier]
                rent /= populationSums[key]
                rent = int(rent//1 + 1)

            # Update the column
            row[rentTier] = rent

        #Concat the row
        filteredRent = filteredRent.append(row, ignore_index=True, sort=False)

# %% Save it
filteredRent.sort_values(['state_alpha', 'countyname'], inplace=True)
filteredRent.index = range(filteredRent.shape[0])
filteredRent.to_csv("./Data/filtered_FY_2016F_50_RevFinal.csv", index=False)
