import pyodbc

conn = pyodbc.connect(
"Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=MovieDB;Trusted_Connection=True;"
)

cursor = conn.cursor()