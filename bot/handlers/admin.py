from database.db_manager import get_role, add_in_bd, delete_in_bd
from keyboards.inline import admin_menu_keyboard, admin_delete_instructor_keyboard, admin_delete_instructor_confirm, \
    get_username


def is_admin(message):
    username = message.from_user.username
    if get_role(username) == 'admin':
        return True
    return False


def register_handlers_admin(bot):

    @bot.message_handler(func = is_admin,  content_types = ['text'], commands = ['admin_menu'])
    def admin_handler(message):
        bot.send_message(message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())

    def take_name_new_instructor(message):
        name = message.text
        bot.send_message(message.chat.id, 'Введите username нового инструктора')
        bot.register_next_step_handler(message, take_username_new_instructor, name)

    def take_username_new_instructor(message, name):
        username = message.text
        bot.send_message(message.chat.id, 'Инструктор успешно добавлен')
        add_in_bd(username=username, role='instructor', name=name)

    @bot.callback_query_handler(func=is_admin)
    def callback_handle_query(call):
        if call.data == 'admin_add_instructor':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Введите имя нового инструктора')
            bot.register_next_step_handler(call.message, take_name_new_instructor)

        elif call.data == 'admin_delete_instructor':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Выберите инструктора для удаления',
                             reply_markup=admin_delete_instructor_keyboard())

        elif 'admin_delete_' in call.data:
            bot.answer_callback_query(call.id)
            markup = admin_delete_instructor_confirm(call)
            bot.send_message(call.message.chat.id, f'Вы уверены, что хотите удалить {call.data[13:]}?',
                             reply_markup=markup)

        elif call.data.startswith('admin_confirm_delete_yes'):
            bot.answer_callback_query(call.id)
            username = call.data.replace('admin_confirm_delete_yes_', '')
            delete_in_bd(username)
            bot.send_message(call.message.chat.id, f'@{username} Удален')
            bot.send_message(call.message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())

        elif call.data.startswith('admin_confirm_delete_no'):
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Удаление отменено')
            bot.send_message(call.message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())
