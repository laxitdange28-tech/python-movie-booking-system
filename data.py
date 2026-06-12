import sqlite3
import pandas as pd

conn = sqlite3.connect("movie.db")

df = pd.read_sql("SELECT * FROM Movies", conn)

print(df)