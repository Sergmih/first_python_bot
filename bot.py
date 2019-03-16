import config
import telebot


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def common_answer(message):
    print('пришло сообщение')
    bot.send_message(config.my_chat_id, 'я не понимаю, но ты все равно пиши чонить)')


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
