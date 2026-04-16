from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager_sql import db



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
    instructors = db.get_all_role('instructor')

    for instructor in instructors:
        button = InlineKeyboardButton(f'{instructor['name']} (@{instructor['username']})', callback_data=f'admin_delete_{instructor['user_id']}')
        markup.row(button)

    return markup


def admin_delete_instructor_confirm(call):
    user_id = call.data.replace('admin_delete_','')

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Да', callback_data = f'admin_confirm_delete_yes_{user_id}')
    button2 = InlineKeyboardButton('Нет', callback_data = 'admin_confirm_delete_no')

    markup.add(button1, button2)
    return markup
