from database.db_manager_sql import db
from keyboards.inline import *
from utils.dates_handler import date_handler, to_group
import json

month_numbers = {
    'december':12,
    'january':1,
    'february':2,
    'march':3,
    'april':4,
    'may':5,
    'june':6,
    'july':7,
    'august':8,
    'september':9,
    'october':10,
    'november':11
}
def is_instructor(message):
    user_id = message.from_user.id
    if db.get_role(user_id) == 'instructor':
        return True
    return False

def register_handlers_instructor(bot):

    @bot.message_handler(func=is_instructor, commands=['instructor_menu'])
    def instructor_menu(message):
        bot.send_message(message.chat.id, 'Меню инструктора:', reply_markup=instructor_menu_keyboard())

    @bot.message_handler(func = lambda message: db.get_action(message.from_user.id) == 'wait_enter_year')
    def wait_enter_year(message):
        year = message.text
        try:
            year = int(year)
        except:
            bot.send_message(message.chat.id, 'Неверный формат, введите год в виде числа')

        action_data = {'year': year}
        data_string = json.dumps(action_data)
        bot.send_message(message.chat.id, 'Выберите месяц', reply_markup=month_menu_keyboard())
        db.add_action_data(message.from_user.id, data_string)
        db.delete_action(message.from_user.id)

    @bot.message_handler(func = lambda msg: db.get_action(msg.from_user.id) == 'wait_enter_day')
    def wait_enter_day(message):
        input_data = message.text
        data = db.get_action_data(message.from_user.id)
        data = json.loads(data)
        data['day'] = input_data
        new_data = json.dumps(data)
        db.add_action_data(message.from_user.id, new_data)

        db.update_action(message.from_user.id, 'wait_enter_time')
        bot.send_message(message.chat.id, '''Введите рабочее время в формате:
- 8-18(c 8 до 18 включительно)
- 8,9,10''')

    @bot.message_handler(func = lambda msg:db.get_action(msg.from_user.id) == 'wait_enter_time')
    def wait_enter_time(message):
        input_data = message.text
        data = db.get_action_data(message.from_user.id)
        data = json.loads(data)
        data['time'] = input_data
        db.delete_action(message.from_user.id)
        bot.send_message(message.chat.id, "Запись успешно открыта")

        good_data = date_handler(data)
        days = good_data['day']
        times = good_data['time']
        teacher_id = message.from_user.id
        for day in days:
            for time in times:
                db.open_lesson(teacher_id, time, day, data['month'], data['year'])
        db.delete_action_data(message.chat.id)

def register_callbacks_handlers_instructor(bot):


    @bot.callback_query_handler(func=is_instructor)
    def callback_handler(call):
        if call.data == 'instructor_new_lessons':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Введите год в формате числа", reply_markup=instructor_cancel_keyboard())
            db.update_action(call.from_user.id, 'wait_enter_year')

        elif call.data == 'instructor_cancel_lesson':
            bot.send_message(call.message.chat.id, f"Какой урок вы бы хотели отменить?", reply_markup=instructor_cancel_lesson(call.from_user.id))

        elif call.data == 'instructor_cancel':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Действие отменено')
            db.delete_action(call.from_user.id)


        elif call.data.startswith('month_'):
            bot.answer_callback_query(call.id)
            month_str = call.data.replace('month_', '')
            month = month_numbers[month_str]
            action_data_old = db.get_action_data(call.from_user.id)
            action_data_new = json.loads(action_data_old)
            action_data_new['month'] = month
            action_data = json.dumps(action_data_new)
            db.add_action_data(call.from_user.id, action_data)

            bot.send_message(call.message.chat.id, '''Введите число/числа в формате: 
- 15(только 15е число)
- 10-15(все дни с 10го до 15го числа включительно)
- 10- (все дни с 10го до конца месяца)
- -10 (все дни с 1го до 10го включительно
- 1,4,5-10(1е, 4е, c 5го до 10го включительно)
- -(весь месяц)''')
            db.update_action(call.from_user.id, 'wait_enter_day')

        elif call.data.startswith('instructor_cancel_lesson_'):
            bot.answer_callback_query(call.id)

            data = call.data.replace('instructor_cancel_lesson_', '')

            date, teacher_id = data.split('_')
            time, day, month, year = date.split('/')


            booked_by = db.get_lesson_booked_by(teacher_id, time, day, month, year)
            db.delete_lesson(teacher_id, time, day, month, year)

            bot.send_message(call.message.chat.id, 'Урок успешно отменен')
            bot.send_message(booked_by, f'Ваш урок {time}:00 {day}.{month}.{year} был отменен инструктором', reply_markup=user_menu_keyboard())
