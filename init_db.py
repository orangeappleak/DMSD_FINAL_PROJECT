import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO admins (username, password) VALUES (?,?)", ('karthik','admin'))
cur.execute("INSERT INTO admins (username, password) VALUES (?,?)", ('admin1','admin1'))
cur.execute("INSERT INTO admins (username, password) VALUES (?,?)", ('admin2','admin2'))

cur.execute("UPDATE TABLE documents SET DOCID == '1' WHERE  DOCID == '2'")
connection.commit()
connection.close()
