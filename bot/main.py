import telebot
from dotenv import load_dotenv
import os
from database.db_manager_sql import db

from handlers.admin import register_handlers_admin,register_callbacks_handlers_admin
from handlers.user import register_handlers_user, register_callbacks_handlers_user
from handlers.instructor import register_handlers_instructor, register_callbacks_handlers_instructor

def main():
    load_dotenv('.env')
    TOKEN = os.getenv('TOKEN')
    if TOKEN is None:
        print('Empty token')
    else:
        try:
            bot = telebot.TeleBot(TOKEN)
            register_handlers_admin(bot)
            register_handlers_user(bot)
            register_handlers_instructor(bot)
            register_callbacks_handlers_instructor(bot)
            register_callbacks_handlers_admin(bot)
            register_callbacks_handlers_user(bot)

            @bot.message_handler(func=lambda msg: db.get_action(msg.from_user.id) == 'nothing')
            def other(message):
                print('other message', message.text)
                bot.send_message(message.chat.id, 'Я вас не понял')

            bot.infinity_polling()
        except:
            print('Failed to connect to Telegram API')

if __name__ == '__main__':
    main()