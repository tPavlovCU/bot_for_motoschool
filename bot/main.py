import telebot
import dotenv
from dotenv import load_dotenv
import os

from handlers.admin import register_handlers_admin
from handlers.user import register_handlers_user

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


            bot.infinity_polling()
        except:
            print('Failed to connect to Telegram API')

if __name__ == '__main__':
    main()