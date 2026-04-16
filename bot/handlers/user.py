import telebot
from database.db_manager import get_role, add_in_bd

def register_handlers_user(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        role = get_role(message.from_user.username)
        if role == 'admin':
            bot.send_message(message.chat.id, 'Привет, админ, чтобы вызвать меню: /admin_menu')

        elif role == 'instructor':
            bot.send_message(message.chat.id, 'Привет, инструктор, чтобы вызвать меню: /instructor_menu')

        elif role == 'user' or role is None:
            bot.send_message(message.chat.id, 'Добро пожаловать в мотошколу Неваляшка, чтобы записаться: /new_reg')
            add_in_bd(message.from_user.username)
