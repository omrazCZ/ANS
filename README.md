# Sports Network Analysis

## Task
Predict performance of basketball matchups between two lineups from Home team and Away team, respectively. 

The dataset can be found at https://www.kaggle.com/datasets/wyattowalsh/basketball as part of a Kaggle Challenge. We provide the data tables transformed into csv files.

Soccer dataset available at https://www.kaggle.com/datasets/hugomathien/soccer as part of a challenge.

Some of the files are too large, therefore we provide a script convert_data.py to generate them localy (assuming you have dowloaded the sqlite files from Kaggle). E.g.

```python convert_data.py archive/database.sqlite soccer_data```


Basketball lineup data can be fetched using the basketball_reference_scraper library with the script

basketball_reference_api.py

## User Guide

... How to generate data ...

To run our models the SportsNetwork.Rmd file can be used directly. 

Note: The cell labeled 'ISM Metrics' takes a long time to recompute and may be skipped.

## Results

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