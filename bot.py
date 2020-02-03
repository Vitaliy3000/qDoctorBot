import os
import time

import telebot as tb


bot = tb.TeleBot(os.environ['TOKEN'])


@bot.message_handler(commands=['authorization'])
def handle_authorization(message):
    bot.send_message(message.from_user.id, 'Отправьте, пожалуйста, ваш номер полиса')
    bot.send_message(message.from_user.id, 'Отправьте, пожалуйста, вашу дату рождения в формате ДД ММ ГГГГ')
    # keyboard = [[tb.InlineKeyboardButton("Записаться", callback_data='1')]]
    # markup = tb.InlineKeyboardMarkup(keyboard)
    markup = types.InlineKeyboardMarkup()
    markup.add(tb.InlineKeyboardButton("Записаться", callback_data='1'))
    bot.send_message(message.from_user.id, 'Пожалуйста выберите:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'test')


@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    bot.send_message(call.from_user.id, str(call))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=0)
        except Exception as e:
            time.sleep(3)