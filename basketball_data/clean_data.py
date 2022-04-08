import pandas as pd

# Read raw data
data = pd.read_csv('ASA All NBA Raw Data.csv')
print(data.shape)

# Drop unwanted columns
data.drop(["PG%","SG%","SF%","PF%","C%","last_60_minutes_per_game_bench","last_60_minutes_per_game_starting","active_position_minutes"], axis=1, inplace=True)
print(data.shape)

# Drop duplicate rows
data.drop_duplicates(subset=['game_id','player_id','player'],keep='first', inplace=True)
print(data.shape)

# Check cleaned data
#test = data.groupby(['game_id'])['starter'].sum().reset_index()
#test.to_csv('test_NBA_Clean_Data.csv', index=False, header=True)

# Save cleaned data
data.to_csv('NBA_Clean_Data.csv', index=False, header=True)

print("Done")