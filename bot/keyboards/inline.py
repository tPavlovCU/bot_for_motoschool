from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager_sql import db



def admin_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Добавить инструктора/админа', callback_data='admin_add_somebody')
    button2 = InlineKeyboardButton('Удалить инструктора', callback_data='admin_delete_instructor')
    button3 = InlineKeyboardButton('Изменить расписание инструктора', callback_data='admin_edit_instructor')
    button4 = InlineKeyboardButton('Удалить данные о человеке', callback_data='admin_delete_user')

    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
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


def admin_add_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Для инструктора', callback_data='admin_add_instructor')
    button2 = InlineKeyboardButton('Для админа', callback_data='admin_add_admin')

    markup.row(button1)
    markup.row(button2)
    return markup

def admin_cancel_keyboard():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Отмена', callback_data='admin_cancel')
    markup.row(btn)
    return markup

def user_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Записаться на занятие', callback_data = 'user_new_lesson')
    button2 = InlineKeyboardButton('Отменить занятие', callback_data='user_cancel_lesson')
    button3 = InlineKeyboardButton('Ввести код приглашения', callback_data = 'user_use_invite_code')

    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    return markup



def instructor_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Открыть запись', callback_data = 'instructor_new_lessons')
    button2 = InlineKeyboardButton('Удалить запись', callback_data = 'instructor_cancel_lesson')

    markup.row(button1)
    markup.row(button2)
    return markup


def month_menu_keyboard():
    markup = InlineKeyboardMarkup()

    december = InlineKeyboardButton("Декабрь", callback_data = 'month_december')
    january = InlineKeyboardButton("Январь", callback_data='month_january')
    february = InlineKeyboardButton("Февраль", callback_data='month_february')

    march = InlineKeyboardButton("Март", callback_data='month_march')
    april = InlineKeyboardButton("Апрель", callback_data='month_april')
    may = InlineKeyboardButton("Май", callback_data='month_may')

    june = InlineKeyboardButton("Июнь", callback_data='month_june')
    july = InlineKeyboardButton("Июль", callback_data='month_july')
    august = InlineKeyboardButton("Август", callback_data='month_august')

    september = InlineKeyboardButton("Сентябрь", callback_data='month_september')
    october = InlineKeyboardButton("Октябрь", callback_data='month_october')
    november = InlineKeyboardButton("Ноябрь", callback_data='month_november')

    markup.row(december,january,february)
    markup.row(march,april,may)
    markup.row(june,july,august)
    markup.row(september,october, november)
    return markup

def instructor_cancel_keyboard():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Отмена', callback_data='instructor_cancel')
    markup.row(btn)
    return markup