import sqlite3

con = sqlite3.connect('data.db', autocommit=True)
cur = con.cursor()