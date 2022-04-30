import numpy as np
import pandas as pd
import sys
import csv
from os import listdir
from os.path import join
import re


pbp_dir = 'basketball_pbp'
lineup_dir = 'lineups'
games = listdir(pbp_dir)


# concat lineups in home teams
lineup_home = pd.DataFrame(columns = [0,1,2,3,4,5,"home_players","home_team"])
for game in games:
    data = pd.read_csv(join(lineup_dir,  'lineups_' + game.split('pbp_')[1] + '_home.csv'), header=None, encoding='utf-8')
    data["home_team"] = re.split(r'_|.csv', game)[2]
    # print(data.shape)
    lineup_home = pd.concat([lineup_home, data], ignore_index=True)

for idx in lineup_home.index:
    lineup_home.at[idx, "home_players"] = set(lineup_home.iloc[idx][0:5])

lineup_home.rename(columns={0:"home_p1",1:"home_p2",2:"home_p3",3:"home_p4",4:"home_p5",5:"home_score",6:"time"},inplace=True)
set_home = set(frozenset(i) for i in lineup_home["home_players"])

print("length of lineups in home: ", len(set_home))
#print(lineup_home)



# concat lineups in away teams
lineup_away = pd.DataFrame(columns = [0,1,2,3,4,5,"away_players","away_team"])
for game in games:
    data = pd.read_csv(join(lineup_dir,  'lineups_' + game.split('pbp_')[1] + '_away.csv'), header=None, encoding='utf-8')
    data["away_team"] = re.split(r'_|.csv', game)[3]
    # print(data.shape)
    lineup_away = pd.concat([lineup_away, data], ignore_index=True)

for idx in lineup_away.index:
    lineup_away.at[idx, "away_players"] = set(lineup_away.iloc[idx][0:5])

lineup_away.rename(columns={0:"away_p1",1:"away_p2",2:"away_p3",3:"away_p4",4:"away_p5",5:"away_score",6:"away_time"},inplace=True)
set_away = set(frozenset(i) for i in lineup_away["away_players"])

print("length of lineups in away: ", len(set_away))
#print(lineup_away)


# get lineups for all games from home & away teams
set_all = set_home.union(set_away)
print("length of all lineups: ", len(set_all))
lineups = pd.concat([lineup_home.rename(columns={"home_players":"players","home_team":"team"})[["players","team"]], lineup_away.rename(columns={'away_players':'players','away_team':'team'})[['players','team']]], ignore_index=True)
lineups = lineups.loc[lineups["players"].drop_duplicates().index].reset_index(drop=True)
lineups.index.name="id"
lineups.to_csv('lineups.csv', index=True, header=True, encoding='utf-8')



# get matchups for all games from home & away teams

all_players = list(frozenset(i) for i in lineups["players"])
print("length of all players: ", len(all_players))

matchups = pd.concat([lineup_home,lineup_away], axis=1)
matchups["weight"] = ""
matchups["type"] = ""

for idx in matchups.index:
    matchups.at[idx, "weight"] = matchups.iloc[idx]["home_score"] - matchups.iloc[idx]["away_score"]
    matchups.at[idx, "type"] = np.sign(matchups.iloc[idx]["weight"])
    matchups.at[idx, "home_players"] = all_players.index(matchups["home_players"][idx])
    matchups.at[idx, "away_players"] = all_players.index(matchups["away_players"][idx])

print(matchups.head())

matchups.drop(['away_time'], axis=1, inplace=True)

matchups.to_csv('matchups.csv', index=False, header=True, encoding='utf-8')

print("Done")