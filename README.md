# Sports Network Analysis - Basketball 


## Task
Predict the results of basketball matchups between two lineups from the Home and Away team, respectively. 

## Introduction 
Our work can be summarized into four parts: _Data Collection, Data Cleaning, Network analysis_ and _Building models_. We also provide a summary of results in _Results_ section.


## Data Collection

### Resources
We consider the entire NBA Season 2018-2019 including the Regular Season and Playoffs. In our terminology, a _lineup_ means five players from the same team playing on the court in a time period, and a _matchup_ means two lineups from opposing teams playing against each other on the court in a time period. The basketball season schedule, Play-By-Play data can be found on [Basketball Reference](https://www.basketball-reference.com/).  

2018-2019 NBA Schedule:

https://www.basketball-reference.com/leagues/NBA_2019_games.html

Matchups and lineups are extracted from the Play-By-Play data. For example, Philadelphia 76ers at Boston Celtics Play-By-Play, October 16, 2018:

https://www.basketball-reference.com/boxscores/pbp/201810160BOS.html

It is a non-trivial task to collect the exact lineups and matchups due to the following facts:

- The five starter players from both teams for each of the four quarters are not provided in Play-By-Play data. 
- The information of changing players is provided implicitly by "Player A enters the game for player B" and there could be multiple players changed at once (possibly on both teams).

### Code and Files
Basketball season schedule, Play-By-Play data can be fetched using the _basketball_reference_scraper_ API with the script:

```basketball_reference_api.py```

Next step, lineups and matchups are extracted using the script:

```get_lineups.py```

The Play-By-Play and lineups per-game data are put in _basketball_pbp_ and _lineups_ folder, respectively. Lineups from the Home team and Away team are separated.

## Data Cleaning

The lineups and matchups data are cleaned using the script:

```generate_network_data.py```

The outputs are two csv files: `lineups.csv` and `matchups.csv`. Lineups provide all the distinct lineups with unique id and the team name. Matchups provide players' names, team name, lineups' id, matchup time, points scored for both teams and their differences as _weight_. The results of matchups as _type_(+1 for a Home team win, -1 for a Home team loss, 0 for tie). 

## Network Analysis

We build a directed network from the cleaned matchups and lineups data. In this network, nodes are distinct lineups and edges are the matchups, which always start from the Home team and point to the Away team. Notice that there could be multiple edges between two nodes with the same direction. Furthermore, we drop the edges corresponding to a _tie_ result since it would include additional bias if we treat them as either win or loss.  

The code is in the R Markdown file: 

```SportsNetwork.Rmd```

Example plots of lineups from two opposing team and their matchups can be seen under the section _Network plots_.

## Models

We tried out several common Machine Learning models with the ISM network features to predict the results of matchups (given the edge and its direction): Logistic Regression (paper's method), SVMs (with different kernels), Gaussian processes, Random forests, etc. 

To generate the ISM features for each distinct pair of nodes, we calculated the positive (negative) in (out) degree for each node and found the length of shortest path in the view of 16 networks.

Also, we group together edges that have the same direction (simply summing up all their scores) and take the sign as the final result for that pair of nodes.  

The features are then used as input to the models.

The code is in the R Markdown file: 

```SportsNetwork.Rmd```

Note: The computation of (un)directed shortest paths takes a long time to recompute.

You can skip this step and continue with the provided csv files in the `results` folder.

Please resume with the cell labelled 'Edge centric generation'.

## Results

Logistic regression
Accuracy: 0.87

Logistic regression (linear penalization)
Accuracy: 0.88

SVM (linear kernel)
Accuracy: 0.92

SVM (polynomial kernel)
Accuracy: 0.53

SVM (RBF kernel)
Accuracy: 0.95 **(most successful)**

SVM (sigmoid kernel)
Accuracy: 0.70

Random forests
Accuracy: 0.85

# Future Work

Add additional input parameters (e.g. plus/minus points, rebounds, etc.).


## Other data 
The folder `basketball_data` contains a dataset that was part of a Kaggle challenge (can be found at https://www.kaggle.com/datasets/wyattowalsh/basketball). We provide the data tables transformed into csv files. The folders `english-premier-league_zip` and `soccer_data` contain sports data that we collected but did not use here, they can be saved for future research. (The soccer dataset is available at https://www.kaggle.com/datasets/hugomathien/soccer).

Some of the files are too large, therefore we provide a script `convert_data.py` to generate them locally (assuming you have downloaded the sqlite files from Kaggle). E.g.:

```python convert_data.py archive/database.sqlite soccer_data```
