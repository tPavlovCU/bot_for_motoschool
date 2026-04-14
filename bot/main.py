import telebot
import dotenv
from dotenv import load_dotenv
import os
from database.db_manager import get_role

from handlers.admin import register_handlers_admin

def main():
    load_dotenv('.env')
    TOKEN = os.getenv('TOKEN')
    if TOKEN is None:
        print('Empty token')
    else:
        try:
            bot = telebot.TeleBot(TOKEN)
            register_handlers_admin(bot)

            @bot.message_handler(commands=['start'])
            def start(message):
                role = get_role(message.from_user.username)
                if role == 'admin':
                    bot.send_message(message.chat.id, 'Привет, админ, чтобы вызвать меню: /admin_menu')
                elif role == 'user' or role is None:

                    bot.send_message(message.chat.id, 'Добро пожаловать в мотошколу Неваляшка, чтобы записаться: /new_reg ')





            bot.infinity_polling()
        except:
            print('Failed to connect to Telegram API')

if __name__ == '__main__':
    main()