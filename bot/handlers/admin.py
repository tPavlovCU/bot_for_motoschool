from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import get_role, get_bd, add_in_bd
from keyboards.inline import admin_menu_keyboard


def is_admin(message):
    username = message.from_user.username
    if get_role(username) == 'admin':
        return True
    return False


def register_handlers_admin(bot):

    @bot.message_handler(func = is_admin,  content_types = ['text'], commands = ['admin_menu'])
    def admin_handler(message):
        bot.send_message(message.chat.id, )
