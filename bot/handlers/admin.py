from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import get_role, get_bd, add_in_bd


def is_admin(message):
    username = message.from_user.username
    if get_role(username) == 'admin':
        return True
    return False


def register_handlers_admin(bot):
    @bot.message_handler(func=is_admin, commands=['add_instructor'])
    def start_new_instructor(message):
        msg = bot.send_message(message.chat.id, 'Введите имя нового инструктора')
        bot.register_next_step_handler(msg, new_instructor_name)

    def new_instructor_name(message):
        name = message.text
        bot.send_message(message.chat.id, 'Введите Username нового инструктора, пример: Timofeeeey')
        bot.register_next_step_handler(message, new_instructor_username, name)

    def new_instructor_username(message, name):
        username = message.text
        if add_in_bd(username, name) == 'was in bd':
            bot.send_message(message.chat.id, 'Человек с таким username уже есть, он будет перезаписан как инструктор')
            # позже сделать подтверждение
        else:
            bot.send_message(message.chat.id, 'Инструктор успешно добавлен')


    @bot.message_handler(func=is_admin, commands = ['delete_instructor'])
    def delete_instructor_start(message):
        bot.send_message(message.chat.id, 'Введите username инструктора, которого хотите удалить')
        bot.register_next_step_handler(message, delete_instructor_verify)

    def delete_instructor_verify(message):
