import sqlite3
import sqlite3 as sql

class DBManager:
    def __init__(self, path):
        self.path = path
        self.conn = sql.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sql.Row
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT DEFAULT NULL,
        role TEXT DEFAULT 'user',
        name TEXT DEFAULT NULL)
        ''')
        cursor.close()

    def add_in_bd(self,user_id, username = None, role = 'user', name=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO users (user_id, username, role, name) VALUES (?, ?, ?, ?)''', (user_id, username, role, name))
        except:
            cursor.execute('''
            SELECT user_id, username, role, name FROM users''')
            res = cursor.fetchone()
            for i in res:
                print('res',i)
        self.conn.commit()
        cursor.close()

    def get_role(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT role FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]


    def get_all_role(self, role):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT user_id, username, name FROM users WHERE role = ?''', (role,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def delete_in_bd(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        DELETE FROM users WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        cursor.close()

    def get_in_bd(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT username, name FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def test_instructors(self, user_id, username, name):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, username, name, role) VALUES (?, ?, ?, ?)''', (user_id, username, name,'instructor'))
        self.conn.commit()
        cursor.close()
        return None


db = DBManager('moto-school.db')

