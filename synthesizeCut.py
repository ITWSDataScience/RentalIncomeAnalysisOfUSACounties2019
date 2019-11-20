# Get the data and important columns
import pandas as pd
df = pd.read_csv("./Datasets/Synthesized datasets/raw_joined_county_data.csv")
df = df[["crime_rate_per_100000", "Rent50_0", "Median household income", "State Code", "State", "County"]]

# Calculate yearly rent as ratio of median income
ratio = pd.Series( [((df.iloc[i]["Rent50_0"]*12)/df.iloc[i]["Median household income"])*100 for i in range(len(df))] )
df = pd.concat((df, ratio.rename("RentPercentOfIncome")), axis=1)
df = df[df["Median household income"].notnull()]
df.to_csv("./Datasets/Synthesized datasets/analysis_county_data.csv", index=False)
