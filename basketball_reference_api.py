## Get data from "https://www.basketball-reference.com/" 


# ## Resources 
# https://github.com/jaebradley/basketball_reference_web_scraper
# 
# https://jaebradley.github.io/basketball_reference_web_scraper 
# 
# https://github.com/jaebradley/basketball_reference_web_scraper/pull/230/files
#
#https://github.com/vishaalagartha/basketball_reference_scraper
#
#https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/API.md





# pip install basketball_reference_web_scraper  // VS code probably doesn't work, then can try to switch to Anaconda
# pip install basketball-reference-scraper

import pandas as pd
from datetime import datetime
import csv

#from basketball_reference_web_scraper import client
#from basketball_reference_web_scraper.data import OutputType, Team
  


from basketball_reference_scraper.seasons import get_schedule, get_standings
from basketball_reference_scraper.pbp import get_pbp


#client.play_by_play(home_team=Team.BOSTON_CELTICS, year=2018, month=10, day=16)
#client.play_by_play(
#      home_team=Team.BOSTON_CELTICS,
#      year=2018, month=10, day=16,
#      output_type=OutputType.CSV,
#      output_file_path="./2018_10_06_BOS_PBP.csv"
#      )



# Get schedules of entire season 2018-2019 (regular season + playoffs)
regular_season = get_schedule(season=2019, playoffs=False)
playoffs = get_schedule(season=2019, playoffs=True)
schedule = pd.concat([regular_season,playoffs])
schedule["DATE"]=schedule["DATE"].dt.date
#schedule['HOME'] = schedule['HOME'].str.upper()
#schedule['VISITOR'] = schedule['VISITOR'].str.upper()

schedule.to_csv('Schedule_2019.csv', index=False, header=True)

# Load team code as dictionary
with open('team_code.csv', newline='') as pscfile:
    reader = csv.reader(pscfile)
    next(reader)
    team_code = dict(reader)


# Get play by play stats
#i = 1300
#test = get_pbp(schedule["DATE"][i], team_code.get(schedule["HOME"][i]), team_code.get(schedule["VISITOR"][i]))

#test.to_csv('pbp_' + str(schedule["DATE"][i]) + '_' + schedule["HOME"][i] + '_' + schedule["VISITOR"][i] + '.csv', index=False, header=True)

failed = 0
failed_games = []

for i in range(schedule.shape[0]):
    try:
        home = team_code.get(schedule["HOME"][i])
        away = team_code.get(schedule["VISITOR"][i])
        game = get_pbp(schedule["DATE"][i], home, away)
        game.to_csv('basketball_pbp/pbp_' + str(schedule["DATE"][i]) + '_' + home + '_' + away + '.csv', index=False, header=True)
    except:
        failed += 1
        failed_games.append(i)

print("Failed games: " + str(failed))
print("Done")