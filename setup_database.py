import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
'''
cursor.execute(create_table_query)


create_personal_details_table_query = '''
CREATE TABLE IF NOT EXISTS personal_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
'''
cursor.execute(create_personal_details_table_query)

connection.commit()
connection.close()
