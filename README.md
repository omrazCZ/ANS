# Sports Network Analysis - Basketball 


## Task
Predict the results of basketball matchups between two lineups from Home team and Away team, respectively. 

## Introduction 
Our work can be summarized into four parts: _Collect data, Clean data, Network analysis_ and _Build models_. And we also provide the summary of results in _Result_ section.


## Collect data

### Resources
We consider the entire NBA Season 2018-2019 including Regular Season and Playoffs. In our terminology, a _lineup_ means five players from the same team playing on the court in a time period, and a _matchup_ means two lineups from opposing teams playing against each other on the court in a time period. Basketball season schedule, Play-By-Play data can be found on [Basketball Reference](https://www.basketball-reference.com/).  

2018-2019 NBA Schedule

https://www.basketball-reference.com/leagues/NBA_2019_games.html

Matchups and lineups are extracted from Play-By-Play data. For example, Philadelphia 76ers at Boston Celtics Play-By-Play, October 16, 2018,

https://www.basketball-reference.com/boxscores/pbp/201810160BOS.html

It is not easy to collect the exact lineups and matchups by noticing the following facts:

- The startups five players from both teams for each of the four quarters are not provided in Play-By-Play data. 
- The information of changing players are provided implicitly by "Player A enters the game for player B" and there could be multiple players changed at once.
- A matchup had to be at the same time period with fixed lineups from both teams.  

### Code and files
Basketball season schedule, Play-By-Play data can be fetched using the _basketball_reference_scraper_ API with the script:

```basketball_reference_api.py```

FNext step, lineups and matchups are extracted using the script:
```get_lineups.py```


The Play-By-Play and lineups per-game data are put in _basketball_pbp_ and _lineups_ folder, respectively. Lineups from Hometeam and Awayteam are separated.

## Clean data
The lineups and matchups data are cleaned using the script:

```generate_network_data.py```

The outputs are two csv files: "lineups.csv" and "matchup.csv". Lineups provide all distinct lineups with unique id and master team's name. Matchups provide players' name, team name, lineups' id, matchup time, scores from both teams and their differences as _weight_, the results of matchups as _type_(+1 for Hometeam win, -1 for Hometeam loss, 0 for tie). 


## Network Analysis

We build a directed network from the cleaned matchups and lineups data. In this network, nodes are distinct lineups and edges are matchups, which always start from Hometeam and point to Awayteam. Notice that there could be multiple edges between two nodes with the same direction. We drops the edges corresponding to a _tie_ result since it will include additional bias if treating them as either win or loss.  

The code is in R Markdown file: 

```SportsNetwork.Rmd```

Example plots of lineups from two opposing team and their matchups can be seen under the section _Network plots_.

## Models
We try out common Machine Learning models with ISM network features to predict the results of matchups(given the edge and its direction): Logistic Regression(paper's method), SVM, Gaussian processes, Light GBM, Random forests, Ensemble, etc. 

To generate the ISM features for each distinct pair of nodes, we calculated the positive(negative) inout) degree for each node and found the length of shortest path in view of 16 networks.

Also, we group by edges that have the same direction by summing up all the scores and take the sign as the final result for that pair of nodes.  

The features are then used as input to the models.

The code is in R Markdown file: 

```SportsNetwork.Rmd```

Note: The cell labeled 'ISM Metrics' takes a long time to recompute and may be skipped.

The generated features are put in the csv file: "edge_centric.csv".

## Result

Logistic regression
Accuracy: 0.86

SVM (linear kernel)
Accuracy: 0.88

SVM (polynomial kernel)
Accuracy: 0.53

SVM (RBF kernel)
Accuracy: 0.97

SVM (sigmoid kernel)
Accuracy: 0.69

### In progress

Random forrests

Ensemble classifiers

Light GBM

Additional input parameters (e.g. matchup duration), or weighing of the ISM metric.



## Other data 
The folder "basketball_data"(The dataset can be found at https://www.kaggle.com/datasets/wyattowalsh/basketball as part of a Kaggle Challenge. We provide the data tables transformed into csv files.), "english-premier-league_zip", "soccer_data"(Soccer dataset available at https://www.kaggle.com/datasets/hugomathien/soccer as part of a challenge.) are sports data that we collected but didn't use here, which can be saved for futuere research. 

Some of the files are too large, therefore we provide a script convert_data.py to generate them localy (assuming you have dowloaded the sqlite files from Kaggle). E.g.

```python convert_data.py archive/database.sqlite soccer_data```
