import sqlite3

conn = sqlite3.connect('database.db')
# print("Opened database successfully")

# conn.execute('CREATE TABLE users (fullname TEXT, email TEXT, username TEXT, password TEXT,mobile INTEGER)')
# print ("Table created successfully")
# conn.close()


cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())