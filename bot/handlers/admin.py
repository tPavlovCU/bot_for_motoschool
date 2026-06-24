from database.db_manager_sql import db
from keyboards.inline import *
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

    @bot.message_handler(commands = ['get_action'])
    def get_action(message):
        bot.send_message(message.chat.id, text=db.get_action(message.from_user.id))

    @bot.message_handler(func = lambda message: db.get_action(message.from_user.id) == 'wait_delete_user_id')
    def wait_delete_user_id(message):
        try:
            result = db.delete_in_bd(int(message.text))
            bot.send_message(message.chat.id, text=result)
            db.delete_action(message.from_user.id)
        except:
            bot.send_message(message.chat.id, text='Неверный user_id, попробуйте еще раз',reply_markup = admin_cancel_keyboard())





def register_callbacks_handlers_admin(bot):

    @bot.callback_query_handler(func=is_admin)
    def callback_handle_query(call):
        if call.data == 'admin_add_somebody':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Какой ключ вы бы хотели создать?", reply_markup = admin_add_keyboard())
        elif call.data == 'admin_cancel':
            bot.answer_callback_query(call.id)
            db.delete_action(call.from_user.id)
            bot.send_message(call.message.chat.id, 'Действие отменено')

        elif call.data == 'admin_add_instructor':
            bot.answer_callback_query(call.id)
            code = generate_instructor_invite_code()
            answer = f'''
            Отправьте этот код инструктору, он должен ввести /invite_code
            
<code>{code}</code>
            '''
            db.add_code(code)
            bot.send_message(call.message.chat.id, answer, parse_mode = 'HTML')

        elif call.data == 'admin_add_admin':
            bot.answer_callback_query(call.id)
            code = generate_admin_invite_code()
            answer = f'''
            Отправьте этот код админу, он должен ввести /invite_code

<code>{code}</code>
            '''
            db.add_code(code)
            bot.send_message(call.message.chat.id, answer, parse_mode='HTML')

        elif call.data == 'admin_delete_user':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Введите user_id человека для удаления', reply_markup = admin_cancel_keyboard())
            db.update_action(call.from_user.id, 'wait_delete_user_id')

        elif call.data == 'admin_edit_instructor':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, 'Выберите инструктора', reply_markup = admin_edit_instructor_keyboard())

        elif 'delete' in call.data:
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

        elif call.data.startswith('admin_edit_instructor_'):
            bot.answer_callback_query(call.id)
            instructor_id = int(call.data.replace('admin_edit_instructor_', ''))
            info = db.get_in_bd(instructor_id)
            name = info['name']
            username = info['username']

            bot.send_message(call.message.chat.id, f"Выбран инструктор {name} (@{username}). Что вы хотите сделать?", reply_markup = admin_edit_select_action_instructor_keyboard(instructor_id))

        elif call.data.startswith('admin_edit_cancel_'):
            bot.answer_callback_query(call.id)
            instructor_id = int(call.data.replace('admin_edit_cancel_', ''))

            bot.send_message(call.message.chat.id, "Какой урок вы бы хотели отменить?", reply_markup = admin_cancel_lesson(instructor_id))

        elif call.data.startswith('admin_edit_lesson_'):
            bot.answer_callback_query(call.id)
            print(call.data)
            date, teacher_id = call.data.replace('admin_edit_lesson_cancel_', '').split('_')

            time, day, month, year = date.split('/')

            booked_by = db.get_lesson_booked_by(teacher_id, time, day, month, year)
            db.delete_lesson(teacher_id, time, day, month, year)

            bot.send_message(call.message.chat.id, 'Урок успешно отменен')
            bot.send_message(booked_by, f'Ваш урок {time}:00 {day}.{month}.{year} был отменен администратором',
                             reply_markup=user_menu_keyboard())

