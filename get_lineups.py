import numpy as np
import pandas as pd
import sys


# Read a play by play file
if len(sys.argv) > 1:
    game = sys.argv[1]
else:
    game = 'pbp_2019-05-17_Milwaukee Bucks_Toronto Raptors.csv'

data = pd.load(game)
print(data.shape)

home_lineups = [['A', 'B', 'C', 'D', 'E']]
away_lineups = [['F', 'G', 'H', 'I', 'J']]

home_score = []
away_score = []

for i in range(data.shape[0]):
    if 'enters' in data[i,2]:
        print('Home Lineup change')
    if 'enters' in data[i,3]:
        print('Away Lineup change')
