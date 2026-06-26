from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager_sql import db
from utils.dates_handler import to_group
from datetime import datetime
import json

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

def admin_edit_instructor_keyboard():
    markup = InlineKeyboardMarkup()
    instructors = db.get_all_role('instructor')

    for instructor in instructors:
        button = InlineKeyboardButton(f'{instructor['name']} (@{instructor['username']})',
                                      callback_data=f'admin_edit_instructor_{instructor['user_id']}')
        markup.row(button)

    return markup

def admin_edit_select_action_instructor_keyboard(instructor_id):
    markup = InlineKeyboardMarkup()
    button_cancel = InlineKeyboardButton('Отменить занятие', callback_data = f'admin_edit_cancel_{instructor_id}')
    button_move = InlineKeyboardButton('Перенести занятие', callback_data = f'admin_edit_move_{instructor_id}')

    markup.row(button_cancel)
    markup.row(button_move)
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

def admin_cancel_lesson(teacher_id):
    markup = InlineKeyboardMarkup()
    lessons = db.get_active_lessons_teacher(teacher_id)


    for lesson in lessons:
        time = lesson['time']
        day = lesson['day']
        month = lesson['month']
        year = lesson['year']

        date = f'{time}/{day}/{month}/{year}'

        btn = InlineKeyboardButton(f"{time}:00 {day}.{month}.{year}", callback_data = f'admin_edit_lesson_cancel_{date}_{teacher_id}')
        markup.row(btn)

        btn = InlineKeyboardButton('Отмена', callback_data='admin_cancel')
        markup.row(btn)

    return markup



def instructor_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Открыть запись', callback_data = 'instructor_new_lessons')
    button2 = InlineKeyboardButton('Удалить запись', callback_data = 'instructor_cancel_lesson')

    markup.row(button1)
    markup.row(button2)
    return markup

def instructor_cancel_keyboard():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Отмена', callback_data='instructor_cancel')
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

def user_select_instructor():
    markup = InlineKeyboardMarkup()
    instructors = db.get_instructors()
    a = instructors[0]

    for instructor in instructors:
        button = InlineKeyboardButton(f'{instructor['name']} (@{instructor['username']})',
                                      callback_data=f'user_select_instructor_{instructor['user_id']}')
        markup.row(button)

    cancel_button = InlineKeyboardButton('Отмена', callback_data='user_select_instructor_-1')
    markup.row(cancel_button)
    return markup

def user_select_day_instructor(instructor_id, user_id, page=0):
    week = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
    markup = InlineKeyboardMarkup()
    days = db.get_instructor_days(instructor_id)
    grouped_days = to_group(days, 5)
    max_pages = len(grouped_days)

    action_data = {'last_page': page, 'max_pages': max_pages, 'instructor_id': instructor_id, 'user_id': user_id}
    db.update_action_data(user_id, action_data)


    try:
        page_data = grouped_days[page]
    except:
        print(grouped_days, page, max_pages)

    for day in page_data:
        date_string = f'{day[0]}/{day[1]}/{day[2]}'
        date_day = datetime.strptime(date_string, '%d/%m/%Y')
        day_month_year = date_string.split('/')
        day_month_year = list(map(lambda x: str(x).zfill(2), day_month_year))
        week_day = week[date_day.weekday()]
        btn = InlineKeyboardButton(f'{day_month_year[0]}.{day_month_year[1]}.{day_month_year[2]} ({week_day})', callback_data=f'user_select_instructor_day_{date_string}_{instructor_id}')
        markup.row(btn)


    btn_next = InlineKeyboardButton('>>', callback_data='user_select_instructor_day_next_page')
    btn_last = InlineKeyboardButton('<<', callback_data='user_select_instructor_day_last_page')
    btn_nthg = InlineKeyboardButton('==', callback_data='nothing')

    markup.row(btn_last, btn_nthg, btn_next)

    cancel_button = InlineKeyboardButton('Отмена', callback_data='user_select_instructor_-1')
    markup.row(cancel_button)
    return markup

def user_select_instructor_time(time, date, instructor_id):
    grouped = to_group(time, 4)
    markup = InlineKeyboardMarkup()
    for group in grouped:
        group_res = []

        for hour in group:
            btn = InlineKeyboardButton(hour, callback_data = f'user_select_instructor_time_{hour}/{date}_{instructor_id}')
            group_res.append(btn)
        markup.row(*group_res)

    cancel_button = InlineKeyboardButton('Отмена', callback_data='user_select_instructor_-1')
    markup.row(cancel_button)
    return markup

def user_cancel_lesson(user_id):
    markup = InlineKeyboardMarkup()
    lessons = db.get_active_lessons(user_id)

    for lesson in lessons:
        teacher_name = db.get_name(lesson['teacher_id'])
        btn_text = f'{lesson['day']}.{lesson['month']}.{lesson['year']} {lesson['time']}:00 {teacher_name}'
        date = f'{lesson['time']}/{lesson['day']}/{lesson['month']}/{lesson['year']}'
        btn = InlineKeyboardButton(btn_text, callback_data=f'user_cancel_lesson_{date}_{lesson['teacher_id']}')
        markup.row(btn)

    cancel_button = InlineKeyboardButton('Назад', callback_data='user_select_instructor_-1')
    markup.row(cancel_button)
    return markup

def instructor_cancel_lesson(teacher_id):
    markup = InlineKeyboardMarkup()
    lessons = db.get_active_lessons_teacher(teacher_id)


    for lesson in lessons:
        time = lesson['time']
        day = lesson['day']
        month = lesson['month']
        year = lesson['year']

        date = f'{time}/{day}/{month}/{year}'

        btn = InlineKeyboardButton(f"{time}:00 {day}.{month}.{year}", callback_data = f'instructor_cancel_lesson_{date}_{teacher_id}')
        markup.row(btn)

    return markup


def admin_select_move_lesson(teacher_id):
    markup = InlineKeyboardMarkup()
    lessons = db.get_active_lessons_teacher(teacher_id)

    for lesson in lessons:
        time = lesson['time']
        day = lesson['day']
        month = lesson['month']
        year = lesson['year']

        date = f'{time}/{day}/{month}/{year}'

        btn = InlineKeyboardButton(f"{time}:00 {day}.{month}.{year}",
                                   callback_data=f'admin_edit_lesson_move_{date}_{teacher_id}')
        markup.row(btn)

        btn = InlineKeyboardButton('Отмена', callback_data='admin_cancel')
        markup.row(btn)

    return markup