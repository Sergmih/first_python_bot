import config
import database
import commands
import telebot


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['log'])
def common_answer(message):
    print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    if message.chat.id == config.my_chat_id:
        config.log_flag = not config.log_flag
        bot.send_message(config.my_chat_id, 'Отправление логов:' + str(config.log_flag))


@bot.message_handler(commands=['help'])
def common_answer(message):
    print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, config.help_message)
    commands.send_me_log(bot, message)


@bot.message_handler(commands=['get'])
def common_answer(message):
    #try:
        print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
        commands.parse_get_command(message, bot)
    #except:
        print('ошибка в команде get')
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте снова')
    #commands.send_me_log(bot, message)


@bot.message_handler(commands=['statistic'])
def common_answer(message):
    try:
        print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
        commands.parse_statistic_command(message, bot)
    except:
        print('какая-то ошибка в statistic')
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуйте снова')
    commands.send_me_log(bot, message)


@bot.message_handler(commands=['start'])
def common_answer(message):
    print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, config.start_message)
    commands.send_me_log(bot, message)


@bot.message_handler(content_types=['text'])
def common_answer(message):
    print('Сообщение: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Неправильная команда')
    commands.send_me_log(bot, message)


@bot.message_handler(content_types=['photo'])
def common_answer(message):
    print('Фотография от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'ооо, а это фотка')


@bot.message_handler(content_types=['sticker'])
def common_answer(message):
    print('Стикер от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'это стикер')


@bot.message_handler(content_types=['document'])
def common_answer(message):
    print('Документ от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Я такое не понимаю')


@bot.message_handler(content_types=['audio'])
def common_answer(message):
    print('Аудиозапись от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Я такое не понимаю')


@bot.message_handler(content_types=['video'])
def common_answer(message):
    print('Видеозапись от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Видео я не умею обрабатывать')


@bot.message_handler(content_types=['voice'])
def common_answer(message):
    print('Голосовуха от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Я такое не понимаю')


@bot.message_handler(content_types=['location'])
def common_answer(message):
    print('локация от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(message.chat.id, 'Я такое не понимаю')


def main():
    bot.send_message(config.my_chat_id, 'Я опять падал')
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
