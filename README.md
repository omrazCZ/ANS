# Sports Network Analysis
Predicting performance of basketball teams

The dataset can be found at https://www.kaggle.com/datasets/wyattowalsh/basketball as part of a Kaggle Challenge. We provide the data tables transformed into csv files.

Soccer dataset available at https://www.kaggle.com/datasets/hugomathien/soccer as part of a challenge.

Some of the files are too large, therefore we provide a script convert_data.py to generate them localy (assuming you have dowloaded the sqlite files from Kaggle). E.g.

```python convert_data.py archive/database.sqlite soccer_data```
