import numpy as np
import pandas as pd
import sqlite3

db_file = 'archive/basketball.sqlite'
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
for table in tables:
    cur = pd.read_sql_query('SELECT * FROM ' + table, con)
    cur.to_csv('basketball_data/' + table + '.csv', index=False)

print("Done")
