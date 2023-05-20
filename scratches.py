import sqlite3

#establish connection
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

#query
cursor.execute("SELECT * FROM events WHERE city='singapore'")
rows = cursor.fetchall()
print(rows)

#insert rows
newrows = [('the heat', 'singapore', '2023.10.10'), ('nangka club', 'KL', '2024.10.10')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", newrows)
connection.commit()

#see all
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)