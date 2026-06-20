from database.db_manager_sql import db
from keyboards.inline import *


def is_user(message):
    user_id = message.from_user.id
    if db.get_role(user_id) == 'user':
        return True
    return False

def register_handlers_user(bot):
    @bot.message_handler(commands=['test'])
    def test(message):
        db.add_in_bd(user_id=1, username='Vladimir', role='instructor', name='Vova', chat_id = 1)
        db.add_in_bd(user_id=2, username='Alexander', role='instructor', name='Alex', chat_id = 2)


    @bot.message_handler(commands=['start'])
    def start(message):
        role = db.get_role(message.from_user.id)
        if role == 'admin':
            bot.send_message(message.chat.id, 'Привет, админ, чтобы вызвать меню: /admin_menu')

        elif role == 'instructor':
            bot.send_message(message.chat.id, 'Привет, инструктор, чтобы вызвать меню: /instructor_menu')

        elif role == 'user':
            bot.send_message(message.chat.id, 'Здравствуйте! Это мотошкола Неваляшка', reply_markup = user_menu_keyboard())
        elif role is None:
            bot.send_message(message.chat.id, 'Добро пожаловать в мотошколу Неваляшка!',reply_markup=user_menu_keyboard())
            db.add_in_bd(user_id=message.from_user.id, username=message.from_user.username, role = 'user', chat_id = message.chat.id)
        db.update_action(message.from_user.id, 'nothing')

    @bot.message_handler(commands=['invite_code'])
    def invite_code(message):
        bot.send_message(message.chat.id, 'Введите ваш код приглашения')
        db.update_action(message.from_user.id, 'wait_enter_invite_code')



    @bot.message_handler(func = lambda message: db.get_action(message.from_user.id) == 'wait_enter_invite_code')
    def get_invite_code(message):
        code = message.text
        is_actual_code = db.activate_code(code)
        if is_actual_code:
            if code[0] == '0':
                db.delete_code(code)
                db.update_action(message.from_user.id, 'wait_enter_instructor_name')
                bot.send_message(message.chat.id, 'Введите ваше имя')
            elif code[0] == '1':
                db.delete_code(code)
                db.update_action(message.from_user.id, 'wait_enter_admin_name')
                bot.send_message(message.chat.id, 'Введите ваше имя')
        else:
            bot.send_message(message.chat.id, 'Такого ключа не существует')


    @bot.message_handler(func = lambda message: db.get_action(message.from_user.id) == 'wait_enter_instructor_name')
    def wait_enter_instructor_name(message):
        name = message.text
        db.add_in_bd(user_id=message.from_user.id, username=message.from_user.username, role='instructor', name=name,
                     chat_id=message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно добавлены в качестве инструктора')

    @bot.message_handler(func = lambda message: db.get_action(message.from_user.id) == 'wait_enter_admin_name')
    def wait_enter_admin_name(message):
        name = message.text
        db.add_in_bd(user_id=message.from_user.id, username=message.from_user.username, role='admin', name=name,
                     chat_id=message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно добавлены в качестве админа')


def register_callbacks_handlers_user(bot):

    @bot.callback_query_handler(func = is_user)
    def callback(call):
        if call.data == 'user_new_lesson':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Выберите инструктора:", reply_markup=user_select_instructor())

        elif call.data.startswith('user_select_instructor_') and not call.data.startswith('user_select_instructor_day') and not call.data.startswith('user_select_instructor_time'):
            bot.answer_callback_query(call.id)
            instructor_id = call.data.replace('user_select_instructor_', '')
            instructor_id = int(instructor_id)
            instructor_name = db.get_name(instructor_id)
            if instructor_id == -1:
                bot.send_message(call.message.chat.id, 'Здравствуйте! Это мотошкола Неваляшка',
                                 reply_markup=user_menu_keyboard())
            else:
                bot.send_message(call.message.chat.id, f"Выбран инструктор {instructor_name}, выберите день:", reply_markup=user_select_day_instructor(instructor_id))
        elif call.data.startswith('user_select_instructor_day') and not call.data.startswith('user_select_instructor_time'):
            bot.answer_callback_query(call.id)
            date, instructor_id = (call.data.replace('user_select_instructor_day_', '')).split('_')

            time = db.get_instructor_time(instructor_id, date)


            bot.send_message(call.message.chat.id, "Выберите время:", reply_markup = user_select_instructor_time(time, date, instructor_id))

        elif call.data.startswith('user_select_instructor_time_'):
            bot.answer_callback_query(call.id)
            data = call.data.replace('user_select_instructor_time_', '')
            date, instructor_id = (data).split('_')
            db.book_lesson(instructor_id, call.from_user.id, date)
            bot.send_message(call.message.chat.id, "Успешная запись")
            bot.send_message(call.message.chat.id, 'Меню',
                             reply_markup=user_menu_keyboard())

        elif call.data == 'user_cancel_lesson':
            bot.answer_callback_query(call.id)

            bot.send_message(call.message.chat.id, 'Какое занятие Вы бы хотели отменить?', reply_markup = user_cancel_lesson(call.from_user.id))

        elif call.data.startswith('user_cancel_lesson_'):
            data = call.data.replace('user_cancel_lesson_', '')
            date, instructor_id = (data).split('_')
            time, day, month, year = date.split('/')
            db.cancel_lesson(instructor_id, time, day, month, year)
            bot.send_message(call.message.chat.id, "Занятие отменено")
            bot.send_message(call.message.chat.id, 'Меню',
                             reply_markup=user_menu_keyboard())
