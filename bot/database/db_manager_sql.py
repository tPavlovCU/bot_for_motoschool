import sqlite3 as sql
from datetime import datetime
import zoneinfo
import json




class DBManager:
    def __init__(self, path):
        self.path = path
        self.conn = sql.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sql.Row
        self.create_table()
    def delete_table(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        self.conn.commit()
        cursor.close()
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT DEFAULT NULL,
        role TEXT DEFAULT 'user',
        name TEXT DEFAULT NULL,
        chat_id TEXT NOT NULL,
        action TEXT DEFAULT 'nothing',
        action_data TEXT DEFAULT NULL)
        ''')


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL)
        ''')



        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        booked_by INTEGER DEFAULT NULL,
        time TEXT NOT NULL,
        day INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        
        FOREIGN KEY (booked_by) REFERENCES users (user_id)
        FOREIGN KEY (teacher_id) REFERENCES users (user_id))
        ''')
        cursor.close()


    def add_in_bd(self, user_id, chat_id, username = None, role = 'user', name=None, ):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT user_id FROM users WHERE user_id = ?''', (user_id,))
        res = cursor.fetchone()
        if res is None:
            cursor.execute('''
            INSERT INTO users (user_id, username, role, name, chat_id) VALUES (?, ?, ?, ?, ?)''', (user_id, username, role, name, chat_id))
            self.conn.commit()
            cursor.close()
        else:
            cursor.execute('''
            UPDATE users SET role = ?, name = ?, username = ? WHERE user_id = ?''', (role, name, username, user_id))
            self.conn.commit()
            cursor.close()

    def get_role(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT role FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
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
        deleted_rows = cursor.rowcount
        self.conn.commit()

        cursor.execute('''
        DELETE FROM lessons WHERE teacher_id = ?''', (user_id,))
        self.conn.commit()

        cursor.execute('''
        UPDATE lessons SET booked_by = NULL WHERE booked_by = ?''', (user_id,))
        self.conn.commit()

        cursor.close()

        if deleted_rows == 1:
            return 'Человек успешно удален'
        elif deleted_rows == 0:
            return 'Человек не найден'
        else:
            print('Удалено человек -', deleted_rows)
            return None

    def get_in_bd(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT user_id, username, name FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result


    def add_code(self,code):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO invite_codes (code) VALUES (?)''', (code,))
        self.conn.commit()
        cursor.close()

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


    def get_action(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT action FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        if result:
            result = result[0]
        else:
            result = None
        cursor.close()
        return result

    def update_action(self, user_id, action):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT action FROM users WHERE user_id = ?''' ,(user_id,))
        res = cursor.fetchone()
        if res is None:
            result = 'Ошибка. Не удалось обновить состояние'
        elif res == action:
            result = 'Состояние уже было нужным'
        else:
            cursor.execute('''
            UPDATE users SET action = ? WHERE user_id = ?''', (action, user_id))
            self.conn.commit()
            cursor.close()
            result = 'Успешно обновлено'
        return result

    def delete_action(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE users SET action = 'nothing' WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        cursor.close()


    def add_action_data(self, user_id, action_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE users SET action_data = ? WHERE user_id = ?''', (action_data, user_id))
        self.conn.commit()
        cursor.close()

    def update_action_data(self, user_id, action_data):
        cursor = self.conn.cursor()
        old_data_json = db.get_action_data(user_id)
        if old_data_json is None:
            db.add_action_data(user_id, json.dumps(action_data))

        else:
            old_data = json.loads(old_data_json)
            for key in action_data:
                value = action_data[key]
                old_data[key] = value
            new_data = json.dumps(old_data)
            cursor.execute('''
            UPDATE users SET action_data = ? WHERE user_id = ?''', (new_data, user_id))
        self.conn.commit()
        cursor.close()


    def get_action_data(self,user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT action_data FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        if result:
            result = result[0]
        else:
            result = None
        cursor.close()
        return result


    def delete_action_data(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE users SET action_data = NULL WHERE user_id = ?''', (user_id,))

    def open_lesson(self, teacher_id, time, day, month, year):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO lessons (teacher_id, time, day, month, year) VALUES (?, ?, ?, ?, ?)''',(teacher_id, time, day, month, year))
        self.conn.commit()
        cursor.close()



    def get_instructors(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT DISTINCT teacher_id FROM lessons WHERE booked_by IS NULL''')
        result = cursor.fetchall()
        cursor.close()
        res = []
        for p in result:
            res.append(p[0])

        result = []
        for teacher_id in res:
            info = db.get_in_bd(teacher_id)
            result.append(info)
        return result

    def get_name(self,user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT name FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_instructor_days(self, instructor_id):
        cursor = self.conn.cursor()
        moscow_zone = zoneinfo.ZoneInfo("Europe/Moscow")
        today = datetime.now(moscow_zone)
        today_day = today.day
        today_month = today.month
        today_year = today.year
        cursor.execute('''
        SELECT DISTINCT day,month,year FROM lessons WHERE booked_by IS NULL AND teacher_id = ? AND ((year > ?) OR (year = ? AND month > ?) OR (year = ? AND month = ? AND day > ?))''',
                       (instructor_id, today_year, today_year, today_month, today_year, today_month, today_day))
        result = list(cursor.fetchall())

        cursor.close()
        res = []
        for t in result:
            res.append([t[0],t[1],t[2]])
        return res

    def get_instructor_time(self, instructor_id, date):
        day, month, year = date.split('/')

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT DISTINCT time FROM lessons WHERE booked_by is NULL AND day = ? AND month = ? AND year = ? AND teacher_id = ?''',(day, month, year, instructor_id))
        result = cursor.fetchall()
        result = list(result)
        result = list(map(lambda x: x[0], result))
        return result

    def get_active_lessons(self, user_id):
        moscow_zone = zoneinfo.ZoneInfo("Europe/Moscow")
        today = datetime.now(moscow_zone)
        today_day = today.day
        today_month = today.month
        today_year = today.year
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT teacher_id, time, day, month, year FROM lessons WHERE booked_by = ? AND ((year > ?) OR (year = ? AND month > ?) OR (year = ? AND month = ? AND day >= ?))''',
                       (user_id, today_year, today_year, today_month, today_year, today_month, today_day))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_active_lessons_teacher(self, teacher_id):
        cursor = self.conn.cursor()
        moscow_zone = zoneinfo.ZoneInfo("Europe/Moscow")
        today = datetime.now(moscow_zone)
        today_day = today.day
        today_month = today.month
        today_year = today.year
        cursor.execute('''
        SELECT booked_by, time, day, month, year FROM lessons WHERE teacher_id = ? AND booked_by IS NOT NULL AND
        ((year > ?) OR (year = ? AND month > ?) OR (year = ? AND month = ? AND day >= ?))''', (teacher_id, today_year, today_year, today_month, today_year, today_month, today_day))
        result = cursor.fetchall()
        cursor.close()
        return result


    def book_lesson(self, instructor_id, user_id, date):
        time, day, month, year = date.split('/')
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE lessons SET booked_by = ? WHERE teacher_id = ? AND time = ? AND day = ? AND month = ? AND year = ?''',
                       (user_id, instructor_id, time, day, month, year))
        self.conn.commit()
        cursor.close()


    def cancel_lesson(self, instructor_id, time, day, month, year):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE lessons SET booked_by = NULL WHERE time = ? AND day = ? AND month = ? AND year = ? AND teacher_id = ?''', (time, day, month, year, instructor_id))
        self.conn.commit()
        cursor.close()


    def delete_lesson(self, instructor_id, time, day, month, year):
        cursor = self.conn.cursor()
        cursor.execute('''
        DELETE FROM lessons WHERE time = ? AND day = ? AND month = ? AND year = ? AND teacher_id = ?''',(time, day, month, year, instructor_id))
        self.conn.commit()
        cursor.close()

    def get_lesson_booked_by(self, teacher_id, time, day, month, year):
        cursor = self.conn.cursor()
        print(teacher_id, time, day, month, year)
        cursor.execute('''
        SELECT booked_by FROM lessons WHERE teacher_id = ? AND time = ? AND day = ? AND month = ? AND year = ?''', (teacher_id, time, day, month, year))
        result = cursor.fetchone()
        cursor.close()
        return result[0]

db = DBManager('moto-school.db')
#db.delete_table('lessons')
db.add_in_bd(1057854960, role = 'instructor', chat_id=1057854960, name='tim', username='timofey')