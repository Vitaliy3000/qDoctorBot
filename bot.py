import os
import time

import telebot

print('init')
print(os.environ['token'])
bot = telebot.TeleBot(os.environ['token'])


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, 'test')


if __name__ == '__main__':
    while True:
        try:
            print('start')
            bot.polling(none_stop=True, timeout=0)
        except Exception as e:
            time.sleep(3)