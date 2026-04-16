import telebot
from database.db_manager_sql import db

admins = ['Timofeeeey']
instructors = []

def register_handlers_user(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        role = db.get_role(message.from_user.id)
        print(role)
        if role == 'admin':
            bot.send_message(message.chat.id, 'Привет, админ, чтобы вызвать меню: /admin_menu')

        elif role == 'instructor':
            bot.send_message(message.chat.id, 'Привет, инструктор, чтобы вызвать меню: /instructor_menu')

        elif role == 'user' or role is None:
            if message.from_user.username in admins:
                bot.send_message(message.chat.id, 'Добро пожаловать, админ, чтобы вызвать меню: /admin_menu')
                db.add_in_bd(message.from_user.id, message.from_user.username, role='admin')

            elif message.from_user.username in instructors:
                bot.send_message(message.chat.id, 'Добро пожаловать, инструктор, чтобы вызвать меню: /instructor_menu')
                db.add_in_bd(message.from_user.id, message.from_user.username, role='instructor')

            else:
                bot.send_message(message.chat.id, 'Добро пожаловать в мотошколу Неваляшка, чтобы записаться: /new_reg')
                db.add_in_bd(message.from_user.id, message.from_user.username, role = 'user')
