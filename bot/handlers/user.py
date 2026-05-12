from database.db_manager_sql import db
from keyboards.inline import user_menu_keyboard


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
            pass

