import sqlite3 as sql

conn = sql.connect('moto-school.db')
cursor = conn.cursor()
conn.row_factory = sql.Row

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
role TEXT DEFAULT 'user',
name TEXT DEFAULT NULL)
''')

def add_in_bd(username, role, name = None):
    cursor.execute('''
    INSERT INTO users (username, role, name) VALUES (?, ?, ?)''', (username, role, name))
    conn.commit()


def get_role(username):
    cursor.execute('''
    SELECT role FROM users WHERE username = ?''', (username,))



def get_all_role(role):
    cursor.execute('''
    SELECT username FROM users WHERE role = ?''', (role,))



def delete_in_bd(username):
    cursor.execute('''
    DELETE FROM users WHERE username = ?''', (username,))
    conn.commit()


