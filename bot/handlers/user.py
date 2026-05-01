from database.db_manager_sql import db
from keyboards.inline import user_menu_keyboard

admins = ['Timofeeeey']
instructors = []

def register_handlers_user(bot):
    @bot.message_handler(commands=['test'])
    def test(message):
        db.add_in_bd(user_id=1, username='Vladimir', role='instructor', name='Vova')
        db.add_in_bd(user_id=2, username='Alexander', role='instructor', name='Alex')


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
            db.add_in_bd(message.from_user.id, message.from_user.username, role = 'user')

    @bot.message_handler(commands=['invite_code'])
    def invite_code(message):
        bot.send_message(message.chat.id, 'Введите ваш код приглашения')
        bot.register_next_step_handler(message, get_invite_code)



    def get_invite_code(message):
        code = message.text
        is_actual_code = db.activate_code(code)
        if is_actual_code:
            if code[0] == '0':
                db.delete_code(code)
                bot.register_next_step_handler(message, get_new_instructor_name)
                bot.send_message(message.chat.id, 'Введите ваше имя')
            elif code[0] == '1':
                db.delete_code(code)
                bot.send_message(message.chat.id, 'Введите ваше имя')
                bot.register_next_step_handler(message, get_new_admin_name)

        else:
            bot.send_message(message.chat.id, 'Такого ключа не существует')

    def get_new_instructor_name(message):
        name = message.text
        db.add_in_bd(user_id=message.from_user.id, username=message.from_user.username, role='instructor', name=name)
        bot.send_message(message.chat.id, 'Вы успешно добавлены в качестве инструктора')

    def get_new_admin_name(message):
        name = message.text
        db.add_in_bd(user_id=message.from_user.id, username=message.from_user.username, role='admin', name=name)
        bot.send_message(message.chat.id, 'Вы успешно добавлены в качестве админа')

