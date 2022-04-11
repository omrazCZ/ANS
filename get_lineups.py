import numpy as np
import pandas as pd
import sys
import csv
from copy import deepcopy, copy

# Read a play by play file
if len(sys.argv) > 1:
    game = sys.argv[1]
else:
    game = 'basketball_pbp/pbp_2018-10-16_BOS_PHI.csv'

data = pd.read_csv(game)
print(data.shape)

start_home = ['A', 'B', 'C', 'D', 'E']
start_away = ['F', 'G', 'H', 'I', 'J']

home_lineups = [copy(start_home)]
away_lineups = [copy(start_away)]

home_lineups1 = [copy(start_home)]
away_lineups1 = [copy(start_away)]
home_lineups2 = [copy(start_home)]
away_lineups2 = [copy(start_away)]
home_lineups3 = [copy(start_home)]
away_lineups3 = [copy(start_away)]
home_lineups4 = [copy(start_home)]
away_lineups4 = [copy(start_away)]

home_score = [0]
away_score = [0]

last_change = '12:0.0'
last_team = None
q = 1

# Go through pbp and extract important info
for i in range(data.shape[0]):
    
    cur_line = data.iloc[i]

    if q != cur_line[0]:
        q = cur_line[0]
        last_change = '12:00'

    if isinstance(cur_line[2], str) and 'enters' in cur_line[2]:
        print('Home Lineup change')

        joining_player = cur_line[2].split(' enters the game for ')[0]
        leaving_player = cur_line[2].split(' enters the game for ')[1]
        
        old_lineup = copy(home_lineups[-1])
        # If old_player is starter
        if leaving_player not in home_lineups[-1]:
            for j in range(5):
                if start_home[j] in home_lineups[-1]:
                    new_lineup = old_lineup
                    for k in range(len(home_lineups)):
                        home_lineups[k][j] = leaving_player
                    new_lineup[j] = joining_player
                    break
        else:
            new_lineup = [i if i != leaving_player else joining_player for i in old_lineup]

        # 2 player changes at once
        if cur_line[1] == last_change:
            if last_team == 'Home':
                home_lineups[-1] = copy(new_lineup)
            else:
                home_lineups.append(new_lineup)
        else:
            away_lineups.append(copy(away_lineups[-1]))
            
            # Get score of previous lineup
            home_score[-1] = cur_line[-2] - sum(home_score[:-1])
            away_score[-1] = cur_line[-1] - sum(away_score[:-1])

            home_score.append(0)
            away_score.append(0)

            # Add new lineup
            home_lineups.append(new_lineup)

        last_change = cur_line[1]
        last_team = 'Home'

    if isinstance(cur_line[3], str) and 'enters' in cur_line[3]:
        print('Away Lineup change')
        
        joining_player = cur_line[3].split(' enters the game for ')[0]
        leaving_player = cur_line[3].split(' enters the game for ')[1]        

        old_lineup = copy(away_lineups[-1])
        # If old_player is starter
        if leaving_player not in away_lineups[-1]:
            for j in range(5):
                if start_away[j] in away_lineups[-1]:
                    new_lineup = old_lineup
                    for k in range(len(away_lineups)):
                        away_lineups[k][j] = leaving_player
                    new_lineup[j] = joining_player
                    break
        else:
            new_lineup = [i if i != leaving_player else joining_player for i in old_lineup]

        # 2 player changes at once
        if cur_line[1] == last_change:
            if last_team == 'Away':
                away_lineups[-1] = copy(new_lineup)
            else:
                away_lineups.append(new_lineup)
        else:
            home_lineups.append(copy(home_lineups[-1]))

            # Get score of previous lineup
            home_score[-1] = cur_line[-2] - sum(home_score[:-1])
            away_score[-1] = cur_line[-1] - sum(away_score[:-1])

            home_score.append(0)
            away_score.append(0)
            
            # Add new lineup
            away_lineups.append(new_lineup)
        
        last_change = cur_line[1]
        last_team = 'Away'

# Fix last score
last_line = data.iloc[-1]
home_score.append(last_line[-2] - sum(home_score[:-1]))
away_score.append(last_line[-1] - sum(away_score[:-1]))

#h_l_s = 

# CHECK FOR PLAYERS ENTERING AT SAME TIME

for i in range(len(home_lineups)):
    home_lineups[i].append(home_score[i])

for i in range(len(away_lineups)):
    away_lineups[i].append(away_score[i])

with open('lineups/lineups_' + game.split('pbp_')[1] + '_home.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(home_lineups)

with open('lineups/lineups_' + game.split('pbp_')[1] + '_away.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(away_lineups)

print("Done")