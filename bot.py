import os
import time

import telebot as tb

from services import Emias


bot = tb.TeleBot(os.environ['TOKEN'])


@bot.message_handler(commands=['authorization'])
def handle_authorization(message):
    bot.send_message(message.from_user.id, 'Отправьте, пожалуйста, ваш номер полиса')
    bot.send_message(message.from_user.id, 'Отправьте, пожалуйста, вашу дату рождения в формате ГГГГ-ММ-ДД')


@bot.message_handler(content_types=['text'], func=lambda message: len(message.text) == 16)
def handle_oms(message):
    global omsNumber
    omsNumber = message.text
    bot.send_message(message.from_user.id, f'oms: {omsNumber}')


@bot.message_handler(content_types=['text'], func=lambda message: len(message.text) == 10)
def handle_date(message):
    global birthDate
    birthDate = message.text
    bot.send_message(message.from_user.id, f'birh: {birthDate}')
    markup = tb.types.InlineKeyboardMarkup()
    markup.add(tb.types.InlineKeyboardButton("Записаться", callback_data='start'))
    bot.send_message(message.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, 'test')


@bot.callback_query_handler(func=lambda call: call.data == 'start')
def handle_departments(call):
    markup = tb.types.InlineKeyboardMarkup()

    for departament in Emias.deparments(omsNumber, birthDate):
        markup.add(tb.types.InlineKeyboardButton(departament['name'], callback_data='dep'+departament['code']))

    bot.send_message(message.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('dep'))
def handle_doctors(call):
    markup = tb.types.InlineKeyboardMarkup()

    code = call.data[3:]
    for doctor in Emias.doctors(omsNumber, birthDate, code):
        markup.add(tb.types.InlineKeyboardButton(doctor['name'], callback_data='doc'+str(doctor['id'])))

    bot.send_message(message.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('doc'))
def handle_doctors(call):
    markup = tb.types.InlineKeyboardMarkup()

    id = int(call.data[3:])
    doctor = Emias.schedule(omsNumber, birthDate, id)
    for day in doctor['scheduleOfDay']:
        for row_schedule in day['scheduleBySlot'][0]['slot']:
            markup.add(tb.types.InlineKeyboardButton(row_schedule['startTime'], callback_data='sch'+str(doctor['id'])))

    bot.send_message(message.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)



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