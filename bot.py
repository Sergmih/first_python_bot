import config
import telebot


bot = telebot.TeleBot(config.token)


def main():
    bot.send_message(config.my_chat_id, 'trying telebot lib')


if __name__ == '__main__':
    main()
