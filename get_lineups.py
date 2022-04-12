import numpy as np
import pandas as pd
import sys
import csv
from copy import deepcopy, copy
from os import listdir
from os.path import join

'''# Read a play by play file
if len(sys.argv) > 1:
    game = sys.argv[1]
else:
    game = 'basketball_pbp/pbp_2018-10-16_BOS_PHI.csv'
'''

pbp_dir = 'basketball_pbp'
games = listdir(pbp_dir)

for game in games:

    data = pd.read_csv(join(pbp_dir, game))
    print(data.shape)

    start_home = ['A', 'B', 'C', 'D', 'E']
    start_away = ['F', 'G', 'H', 'I', 'J']

    home_lineups = [copy(start_home)]
    away_lineups = [copy(start_away)]

    hl = [[copy(start_home)],[copy(start_home)],[copy(start_home)],[copy(start_home)]]
    al = [[copy(start_away)],[copy(start_away)],[copy(start_away)],[copy(start_away)]]

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
    q = 0

    # To collect names of players that weren't swapped in whole quarter
    potential_home = []
    potential_away = []
    plyr_actions_1 = [' misses ', ' makes ']
    plyr_actions_2 = ['Defensive rebound by ', 'Turnover by ', 'drawn by ', 'assit by ']

    # Go through pbp and extract important info
    for i in range(data.shape[0]):
        
        cur_line = data.iloc[i]

        # Don't consider overtime situations
        if cur_line[0] == '1OT':
            break

        if q != int(cur_line[0]) - 1:
            
            potential_home = list(set(potential_home))
            potential_away = list(set(potential_away))
            # Add non-changed players
            for plyr in potential_home:
                if not any(plyr in l for l in hl[q]):
                    for j in range(5):
                        if hl[q][-1][j] in start_home:
                            for k in range(len(hl[q])):
                                hl[q][k][j] = plyr
                            break
            
            for plyr in potential_away:
                if not any(plyr in l for l in al[q]):
                    for j in range(5):
                        if al[q][-1][j] in start_away:
                            for k in range(len(al[q])):
                                al[q][k][j] = plyr
                            break
            
            potential_home = []
            potential_away = []

            q = int(cur_line[0]) - 1
            last_change = '12:00'

            last_line = data.iloc[i - 1]
            home_score.append(last_line[-2] - sum(home_score[:-1]))
            away_score.append(last_line[-1] - sum(away_score[:-1]))

        if isinstance(cur_line[2], str) and 'enters' in cur_line[2]:
            #print('Home Lineup change')

            joining_player = cur_line[2].split(' enters the game for ')[0]
            leaving_player = cur_line[2].split(' enters the game for ')[1]

            potential_home = [p for p in potential_home if p is not joining_player]
            
            '''old_lineup = copy(home_lineups[-1])
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
                new_lineup = [i if i != leaving_player else joining_player for i in old_lineup]'''
            
            old_l = copy(hl[q][-1])
            # If old_player is starter
            if leaving_player not in hl[q][-1]:
                for j in range(5):
                    if start_home[j] in hl[q][-1]:
                        new_lineup = copy(old_l)
                        for k in range(len(hl[q])):
                            hl[q][k][j] = leaving_player
                        new_lineup[j] = joining_player
                        break
            else:
                new_lineup = [i if i != leaving_player else joining_player for i in old_l]

            # 2 player changes at once
            if cur_line[1] == last_change:
                #if last_team == 'Home':
                    hl[q][-1] = copy(new_lineup)
                #else:
                #    hl[q].append(new_lineup)
            else:
                al[q].append(copy(al[q][-1]))
                
                # Get score of previous lineup
                home_score[-1] = cur_line[-2] - sum(home_score[:-1])
                away_score[-1] = cur_line[-1] - sum(away_score[:-1])

                home_score.append(0)
                away_score.append(0)

                # Add new lineup
                hl[q].append(new_lineup)

            '''# 2 player changes at once
            if cur_line[1] == last_change:
                if last_team == 'Home':
                    home_lineups[-1] = copy(new_lineup)
                #else:
                #    home_lineups.append(new_lineup)
            else:
                away_lineups.append(copy(away_lineups[-1]))
                
                # Get score of previous lineup
                home_score[-1] = cur_line[-2] - sum(home_score[:-1])
                away_score[-1] = cur_line[-1] - sum(away_score[:-1])

                home_score.append(0)
                away_score.append(0)

                # Add new lineup
                home_lineups.append(new_lineup)'''

            last_change = cur_line[1]
            last_team = 'Home'

        if isinstance(cur_line[3], str) and 'enters' in cur_line[3]:
            #print('Away Lineup change')
            
            joining_player = cur_line[3].split(' enters the game for ')[0]
            leaving_player = cur_line[3].split(' enters the game for ')[1]        

            potential_away = [p for p in potential_away if p is not joining_player]

            '''old_lineup = copy(away_lineups[-1])
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
                new_lineup = [i if i != leaving_player else joining_player for i in old_lineup]'''

            old_l = copy(al[q][-1])
            # If old_player is starter
            if leaving_player not in al[q][-1]:
                for j in range(5):
                    if start_away[j] in al[q][-1]:
                        new_lineup = copy(old_l)
                        for k in range(len(al[q])):
                            al[q][k][j] = leaving_player
                        new_lineup[j] = joining_player
                        break
            else:
                new_lineup = [i if i != leaving_player else joining_player for i in old_l]

            # 2 player changes at once
            if cur_line[1] == last_change:
                #if last_team == 'Home':
                    al[q][-1] = copy(new_lineup)
                #else:
                #    al[q].append(new_lineup)
            else:
                hl[q].append(copy(hl[q][-1]))
                
                # Get score of previous lineup
                home_score[-1] = cur_line[-2] - sum(home_score[:-1])
                away_score[-1] = cur_line[-1] - sum(away_score[:-1])

                home_score.append(0)
                away_score.append(0)

                # Add new lineup
                al[q].append(new_lineup)

            '''# 2 player changes at once
            if cur_line[1] == last_change:
                if last_team == 'Away':
                    away_lineups[-1] = copy(new_lineup)
                #else:
                #    away_lineups.append(new_lineup)
            else:
                home_lineups.append(copy(home_lineups[-1]))

                # Get score of previous lineup
                home_score[-1] = cur_line[-2] - sum(home_score[:-1])
                away_score[-1] = cur_line[-1] - sum(away_score[:-1])

                home_score.append(0)
                away_score.append(0)
                
                # Add new lineup
                away_lineups.append(new_lineup)'''
            
            last_change = cur_line[1]
            last_team = 'Away'

        if isinstance(cur_line[2], str):
            if ' misses ' in cur_line[2]:
                plyr = cur_line[2].split(' misses ')[0]
                if not any(plyr in l for l in hl[q]):
                    potential_home.append(plyr)
            elif ' makes ' in cur_line[2]:
                plyr = cur_line[2].split(' makes ')[0]
                if not any(plyr in l for l in hl[q]):
                    potential_home.append(plyr)
        
        if isinstance(cur_line[3], str):
            if ' misses ' in cur_line[3]:
                plyr = cur_line[3].split(' misses ')[0]
                if not any(plyr in l for l in al[q]):
                    potential_away.append(plyr)
            elif ' makes ' in cur_line[3]:
                plyr = cur_line[3].split(' makes ')[0]
                if not any(plyr in l for l in al[q]):
                    potential_away.append(plyr)

    potential_home = list(set(potential_home))
    potential_away = list(set(potential_away))
    # Add non-changed players
    for plyr in potential_home:
        if not any(plyr in l for l in hl[q]):
            for j in range(5):
                if hl[q][-1][j] in start_home:
                    for k in range(len(hl[q])):
                        hl[q][k][j] = plyr
                    break

    for plyr in potential_away:
        if not any(plyr in l for l in al[q]):
            for j in range(5):
                if al[q][-1][j] in start_away:
                    for k in range(len(al[q])):
                        al[q][k][j] = plyr
                    break

    # Fix last score
    last_line = data.iloc[-1]
    home_score[-1] = last_line[-2] - sum(home_score[:-1])
    away_score[-1] = last_line[-1] - sum(away_score[:-1])

    # COLLECT NON-CHANGED PLAYER NAMES

    home_final = [lineup for sublist in hl for lineup in sublist]
    away_final = [lineup for sublist in al for lineup in sublist]

    for i in range(len(home_final)):
        home_final[i].append(home_score[i])

    for i in range(len(away_final)):
        away_final[i].append(away_score[i])

    '''home_final = []
    away_final = []
    for i in range(len(home_lineups)):
        home_final.append(copy(home_lineups[i][:6]))

    for i in range(len(away_lineups)):
        away_final.append(copy(away_lineups[i][:6]))'''

    with open('lineups/lineups_' + game.split('pbp_')[1] + '_home.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(home_final)

    with open('lineups/lineups_' + game.split('pbp_')[1] + '_away.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(away_final)

print("Done")