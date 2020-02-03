import os
import time

import telebot as tb

from services import Emias
# import database


bot = tb.TeleBot(os.environ['TOKEN'])
USERS = {}


def condition_omsNumber(message):
    return len(message.text) == 16 and message.text.isdigit()


def parse_birthDate(message):
    try:
        day, month, year = message.text.split()
        return f'{year}-{month}-{day}' 
    except:
        return None


@bot.message_handler(commands=['authorization'])
def handle_authorization(message):
    bot.send_message(message.from_user.id, 'Отправьте, пожалуйста, ваш номер полиса')


@bot.message_handler(content_types=['text'], func=condition_omsNumber)
def handle_oms(message):
    user_id = message.from_user.id
    USERS[user_id] = {'omsNumber': message.text}
    bot.send_message(user_id, 'Отправьте, пожалуйста, вашу дату рождения в формате ДД ММ ГГГГ')


@bot.message_handler(content_types=['text'], func=parse_birthDate)
def handle_date(message):
    user_id = message.from_user.id
    USERS[user_id] = USERS.get(user_id, {}).update({'birthDate': parse_birthDate(message)})
    print(USERS)
    omsNumber = USERS[user_id]['omsNumber']
    birthDate = USERS[user_id]['birthDate']

    bot.send_message(user_id, f"Проверьте правильность введенных вами данных:\nПолис: {omsNumber}\nДата рождения:{birthDate}")
    markup = tb.types.ReplyKeyboardMarkup()
    markup.add(
        tb.types.KeyboardButton('Верно'),
        tb.types.KeyboardButton('/authorization'),
    )
    bot.send_message(user_id, reply_markup=markup)

@bot.message_handler(content_types=['text'], func=lambda m: m.text == 'Верно')
def handle_true(message):
    user_id = message.from_user.id
    # database.add(user_id, USERS.pop[user_id])
    markup = tb.types.InlineKeyboardMarkup()
    markup.add(tb.types.InlineKeyboardButton("Записаться", callback_data='departments'))
    bot.send_message(user_id, 'Пожалуйста выберите дейтвие (у вас очень большой выбор:):', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, 'Я вас не понимаю')


@bot.callback_query_handler(func=lambda call: call.data == 'departments')
def handle_departments(call):
    user_id = call.from_user.id
    omsNumber = USERS[user_id]['omsNumber']
    birthDate = USERS[user_id]['birthDate']

    markup = tb.types.InlineKeyboardMarkup()

    for departament in Emias.deparments(omsNumber, birthDate):
        markup.add(tb.types.InlineKeyboardButton(departament['name'], callback_data='dep'+departament['code']))

    markup.add(tb.types.InlineKeyboardButton("<- Назад", callback_data="start"))

    bot.send_message(call.from_user.id, 'Пожалуйста выберите департамент:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('dep'))
def handle_doctors(call):
    user_id = call.from_user.id
    omsNumber = USERS[user_id]['omsNumber']
    birthDate = USERS[user_id]['birthDate']

    markup = tb.types.InlineKeyboardMarkup()

    code = call.data[3:]
    for doctor in Emias.doctors(omsNumber, birthDate, code):
        id = doctor['id']
        complexResource = doctor['complexResource'][0]['id']
        code = doctor['receptionType'][0]['code']
        markup.add(tb.types.InlineKeyboardButton(doctor['name'], callback_data=f"doc{id}|{complexResource}|{code}"))

    bot.send_message(call.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('doc'))
def handle_schedule(call):
    user_id = call.from_user.id
    omsNumber = USERS[user_id]['omsNumber']
    birthDate = USERS[user_id]['birthDate']

    markup = tb.types.InlineKeyboardMarkup()

    doctor = call.data[3:]
    id = doctor.split('|')[0]
    doctor = Emias.schedule(omsNumber, birthDate, int(id))
    for day in doctor['scheduleOfDay']:
        for row_schedule in day['scheduleBySlot'][0]['slot']:
            startTime = row_schedule['startTime']
            endTime = row_schedule['endTime']
            print(len(f"sch{doctor}|{startTime}|{endTime}"))
            markup.add(tb.types.InlineKeyboardButton(startTime, callback_data=f"sch{doctor}|{startTime}|{endTime}"))

    bot.send_message(call.from_user.id, 'Пожалуйста выберите время:', reply_markup=markup)



# @bot.callback_query_handler(func=lambda call: True)
# def test_callback(call):
#     bot.send_message(call.from_user.id, str(call))
#     departaments = 
#     return


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=0)
        except Exception as e:
            time.sleep(3)