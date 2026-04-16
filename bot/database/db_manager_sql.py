import sqlite3
import sqlite3 as sql

class DBManager:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sql.Row
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        name TEXT DEFAULT NULL)
        ''')

    def add_in_bd(self,user_id, username, role = 'user', name=None):
        self.cursor.execute('''
            INSERT INTO users (user_id, username, role, name) VALUES (?, ?, ?, ?)''', (user_id, username, role, name))
        self.conn.commit()

    def get_role(self, username):
        self.cursor.execute('''
        SELECT role FROM users WHERE username = ?''', (username,))
        result = self.cursor.fetchone()
        return result

    def get_all_role(self, role):
        self.cursor.execute('''
        SELECT username FROM users WHERE role = ?''', (role,))
        result = self.cursor.fetchall()
        return result

    def delete_in_bd(self, username):
        self.cursor.execute('''
        DELETE FROM users WHERE username = ?''', (username,))
        self.conn.commit()

db = DBManager('../database/moto-school.db')