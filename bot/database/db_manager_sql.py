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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL)
        ''')
        cursor.close()

    # def add_in_bd(self,user_id, username = None, role = 'user', name=None):
    #     cursor = self.conn.cursor()
    #     try:
    #         cursor.execute('''
    #         INSERT INTO users (user_id, username, role, name) VALUES (?, ?, ?, ?)''', (user_id, username, role, name))
    #     except:
    #         cursor.execute('''
    #         SELECT user_id, username, role, name FROM users''')
    #         res = cursor.fetchone()
    #         for i in res:
    #             print('res',i)
    #     self.conn.commit()
    #     cursor.close()

    def add_in_bd(self, user_id, username = None, role = 'user', name=None):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT user_id FROM users WHERE user_id = ?''', (user_id,))
        res = cursor.fetchone()
        if res is None:
            cursor.execute('''
            INSERT INTO users (user_id, username, role, name) VALUES (?, ?, ?, ?)''', (user_id, username, role, name))
        else:
            cursor.execute('''
            UPDATE users SET role = ? WHERE user_id = ?''', (role, user_id))
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

    def activate_code(self, code):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id FROM invite_codes WHERE code = ?''', (code,))
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return False
        else:
            return True


    def delete_code(self, code):
        cursor = self.conn.cursor()
        cursor.execute('''
        DELETE FROM invite_codes WHERE code = ?''', (code,))
        self.conn.commit()
        cursor.close()


db = DBManager('moto-school.db')

