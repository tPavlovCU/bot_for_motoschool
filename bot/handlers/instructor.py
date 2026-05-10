from database.db_manager_sql import db
from keyboards.inline import instructor_menu_keyboard, month_menu_keyboard

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
        bot.send_message(message.chat.id, 'Меню инструктора:', reply_markup=instructor_menu_keyboard)






def register_callbacks_handlers_instructor(bot):
    def get_year(message):
        year = message.text
        try:
            year = int(year)
            bot.send_message(message.chat.id, 'Выберите месяц', reply_markup=month_menu_keyboard())
        except:
            bot.send_message(message.chat.id, 'Неверный формат, введите год в виде числа')


    @bot.callback_query_handler(func=is_instructor)
    def callback_handler(call):
        if call.data == 'instructor_new_lessons':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "Введите год в формате числа")
            bot.register_next_step_handler(call.message, get_year)

        elif call.data.startswith('month_'):
            month_str = call.data.replace('month_', '')
            month = month_numbers[month_str]



