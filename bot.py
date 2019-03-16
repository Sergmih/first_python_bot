import config
import telebot


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def common_answer(message):
    print('пришло обычное сообщение')
    bot.send_message(config.my_chat_id, message.text)


@bot.message_handler(content_types=['photo'])
def common_answer(message):
    print('пришла фотография')
    bot.send_message(config.my_chat_id, 'ооо, а это фотка')

@bot.message_handler(content_types=['sticker'])
def common_answer(message):
    print('пришел стикер')
    bot.send_message(config.my_chat_id, 'это стикер')


@bot.message_handler(content_types=['document'])
def common_answer(message):
    print('пришел документ')
    bot.send_message(config.my_chat_id, 'это документик')


@bot.message_handler(content_types=['audio'])
def common_answer(message):
    print('пришла аудиозапись')
    bot.send_message(config.my_chat_id, 'аудиозапись')


@bot.message_handler(content_types=['commands'])
def common_answer(message):
    print('пришла команда')
    bot.send_message(config.my_chat_id, 'а вот команды я пока не умею обрабатывать')


def main():
    bot.send_message(config.my_chat_id, 'дратути, я умею распознавать тип сообщений')
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
