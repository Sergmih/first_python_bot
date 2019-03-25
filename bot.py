import config
import telebot


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['help'])
def common_answer(message):
    print('Команда ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'а вот команды я пока не умею обрабатывать')


@bot.message_handler(content_types=['text'])
def common_answer(message):
    print('Сообщение ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, message.text)


@bot.message_handler(content_types=['photo'])
def common_answer(message):
    print('Фотография от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'ооо, а это фотка')


@bot.message_handler(content_types=['sticker'])
def common_answer(message):
    print('Стикер ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'это стикер')


@bot.message_handler(content_types=['document'])
def common_answer(message):
    print('Документ от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'это документик')


@bot.message_handler(content_types=['audio'])
def common_answer(message):
    print('Аудиозапись от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'аудиозапись')


def main():
    bot.send_message(config.my_chat_id, 'дратути, я умею распознавать тип сообщений')
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
