from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager_sql import get_all_role

def get_username(s):
    try:
        s = s[s.index('@'):]
        s = s.replace(')', '')
    except:
        print('get_username', s)
    return s


def admin_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Добавить инструктора', callback_data='admin_add_instructor')
    button2 = InlineKeyboardButton('Удалить инструктора', callback_data='admin_delete_instructor')
    button3 = InlineKeyboardButton('Изменить расписание инструктора', callback_data='admin_edit_instructor')

    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    return markup


def admin_delete_instructor_keyboard():
    markup = InlineKeyboardMarkup()
    instructors = get_all_role('instructor')
    for instructor in instructors:
        button = InlineKeyboardButton(instructor, callback_data=f'admin_delete_{get_username(instructor)}')
        markup.row(button)
    return markup


def admin_delete_instructor_confirm(call):
    username = call.data.replace('admin_delete_@','')
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Да', callback_data = f'admin_confirm_delete_yes_{username}')
    button2 = InlineKeyboardButton('Нет', callback_data = 'admin_confirm_delete_no')
    markup.add(button1, button2)
    return markup
