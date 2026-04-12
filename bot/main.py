import telebot
import dotenv
from dotenv import load_dotenv
import os

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

            bot.infinity_polling()
        except:
            print('Failed to connect to Telegram API')

if __name__ == '__main__':
    main()