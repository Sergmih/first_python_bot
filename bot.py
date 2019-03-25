import config
import database
import commands
import telebot


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['help'])
def common_answer(message):
    print('Команда: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'а вот команды я пока не умею обрабатывать')
    commands.get_list_of_currency(bot)


@bot.message_handler(content_types=['text'])
def common_answer(message):
    print('Сообщение: ' + message.text + ' от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, message.text)


@bot.message_handler(content_types=['photo'])
def common_answer(message):
    print('Фотография от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'ооо, а это фотка')


@bot.message_handler(content_types=['sticker'])
def common_answer(message):
    print('Стикер от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'это стикер')
    commands.get_current_rate('USD', bot)


@bot.message_handler(content_types=['document'])
def common_answer(message):
    print('Документ от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'это документик')


@bot.message_handler(content_types=['audio'])
def common_answer(message):
    print('Аудиозапись от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'аудиозапись')


@bot.message_handler(content_types=['video'])
def common_answer(message):
    print('Видеозапись от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'видосики я не умею обрабатывать, соре')


@bot.message_handler(content_types=['voice'])
def common_answer(message):
    print('Голосовуха от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'такое я не понимаю')


@bot.message_handler(content_types=['location'])
def common_answer(message):
    print('локация от ' + message.from_user.first_name + ' ' + message.from_user.last_name + '\n')
    bot.send_message(config.my_chat_id, 'нене, давай по сценарию')


def main():
    bot.send_message(config.my_chat_id, 'Я опять падал')
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
