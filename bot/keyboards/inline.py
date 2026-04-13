from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Добавить инструктора', callback_data='admin_add_instructor')
    button2 = InlineKeyboardButton('')