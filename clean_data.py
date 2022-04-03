import pandas as pd

# Read raw data
data = pd.read_csv('ASA All NBA Raw Data.csv')
print(data.shape)

# Drop unwanted columns
data.drop(["PG%","SG%","SF%","PF%","C%"], axis=1, inplace=True)
print(data.shape)

# Drop duplicate rows
data.drop_duplicates(keep='first', inplace=True)
print(data.shape)

# Save cleaned data
data.to_csv('NBA_Clean_Data.csv', index=False, header=True)

print("Done")