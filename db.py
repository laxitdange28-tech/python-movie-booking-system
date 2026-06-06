import sqlite3

conn = sqlite3.connect(
    "movie.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Movies(
    MovieId INTEGER PRIMARY KEY AUTOINCREMENT,
    MovieName TEXT UNIQUE,
    AvailableSeats INTEGER
)
""")

conn.commit()