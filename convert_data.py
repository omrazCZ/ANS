import imp
import numpy as np
import pandas as pd
import sqlite3
import sys
import os
from os.path import isdir, join

db_file = sys.argv[1]
dest_folder = sys.argv[2]

#db_file = 'archive/basketball.sqlite'
#dest_folder = 'basketball_data/'

# Read DB file
con = sqlite3.connect(db_file, isolation_level=None,
                      detect_types=sqlite3.PARSE_COLNAMES)
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Collect all table names
t = cursor.fetchall()
tables = [i[0] for i in t]
print(tables)

# Store data in csv files
if not isdir(join(os.getcwd(), dest_folder)):
    os.mkdir(dest_folder)

for table in tables:
    cur = pd.read_sql_query('SELECT * FROM ' + table, con)
    cur.to_csv(join(dest_folder, table + '.csv'), index=False)

print("Done")
