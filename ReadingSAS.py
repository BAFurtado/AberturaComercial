# https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/
# https://www.tutorialspoint.com/sqlite/sqlite_syntax.htm

# Basically
# Importing libraries
import datetime as dt

import pandas as pd
from sqlalchemy import create_engine # database connection

# Visualizing table
print(pd.read_csv('//sasworkspace1/publico/Bernardo Alves Furtado (Dirur)/RAIS/mg09.csv', nrows=10).head())

# Creating engine
disk_engine = create_engine('sqlite:///mg09.db')  # Initialize database with filename

# Reading in CHUNKS
start = dt.datetime.now()
chunksize = 50000

j = 0
index_start = 1

for df in pd.read_csv('mg09.csv', chunksize=chunksize,
                      iterator=True, encoding='utf-8', sep=";"):

    df.index += index_start

    # Keep the interesting columns
    columns = ['SBCL_CNAE20', 'PIS', 'EMP_31DEZ']

    for c in df.columns:
        if c not in columns:
            df = df.drop(c, axis=1)


    j += 1
    print('{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j * chunksize))

    df.to_sql('data', disk_engine, if_exists='append')
    index_start = df.index[-1] + 1

df = pd.read_sql_query('SELECT * FROM data LIMIT 10', disk_engine)
df

# Previewing the table. Now from this moment forward everything is just like SQL

df = pd.read_sql_query('SELECT SBCL_CNAE20, COUNT(*) AS NUM_EMPL '
                       'FROM data '
                       'WHERE EMP_31DEZ==1 '
                       'GROUP BY SBCL_CNAE20', disk_engine)
df

