from database.db_manager_sql import db
from keyboards.inline import admin_menu_keyboard, admin_delete_instructor_keyboard, admin_delete_instructor_confirm, admin_add_keyboard
from utils.invite_codes import generate_instructor_invite_code, generate_admin_invite_code

def is_admin(message):
    user_id = message.from_user.id
    if db.get_role(user_id) == 'admin':
        return True
    return False


def register_handlers_admin(bot):

    @bot.message_handler(func = is_admin,  content_types = ['text'], commands = ['admin_menu'])
    def admin_handler(message):
        bot.send_message(message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())




    @bot.callback_query_handler(func=is_admin)
    def callback_handle_query(call):
        if call.data == 'admin_add_somebody':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Какой ключ вы бы хотели создать?", reply_markup = admin_add_keyboard())

        elif call.data == 'admin_add_instructor':
            bot.answer_callback_query(call.id)
            code = generate_instructor_invite_code()
            answer = f'''
            Отправьте этот код инструктору, он должен ввести /invite_code
            
<code>{code}</code>
            '''
            bot.send_message(call.message.chat.id, answer, parse_mode = 'HTML')

        elif call.data == 'admin_add_admin':
            bot.answer_callback_query(call.id)
            code = generate_admin_invite_code()
            answer = f'''
            Отправьте этот код админу, он должен ввести /invite_code

<code>{code}</code>
            '''
            bot.send_message(call.message.chat.id, answer, parse_mode='HTML')


        if 'delete' in call.data:
            if call.data == 'admin_delete_instructor':
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, 'Выберите инструктора для удаления',
                                 reply_markup=admin_delete_instructor_keyboard())

            elif call.data.startswith('admin_delete_'):
                bot.answer_callback_query(call.id)
                data_without_start = call.data.replace('admin_delete_', '')
                info = db.get_in_bd(data_without_start)
                name = info['name']
                username = info['username']
                markup = admin_delete_instructor_confirm(call)
                bot.send_message(call.message.chat.id, f'Вы уверены, что хотите удалить {name} (@{username})?',
                                 reply_markup=markup)

            elif call.data.startswith('admin_confirm_delete_yes'):
                bot.answer_callback_query(call.id)
                user_id = call.data.replace('admin_confirm_delete_yes_', '')
                info = db.get_in_bd(user_id)
                db.delete_in_bd(user_id)
                name = info['name']
                username = info['username']
                bot.send_message(call.message.chat.id, f'Инстркутор {name} (@{username}) Удален')
                bot.send_message(call.message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())

            elif call.data.startswith('admin_confirm_delete_no'):
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, 'Удаление отменено')
                bot.send_message(call.message.chat.id, 'Админ-панель', reply_markup=admin_menu_keyboard())


