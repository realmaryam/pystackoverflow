import telebot
import os
from loguru import logger
from src.utils.io import write_json
from src.constants import keyboards
import emoji


class Bot:
    """
    Telegram bot to randomly connect people to talk
    """
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ['ANONYMOUS_BOT_TOKEN'])
        self.echo_all = self.bot.message_handler(
            func=lambda message: True
        )(self.echo_all)

    def run(self):
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def echo_all(self, message):
        write_json(message.json, 'data/message.json')
        # print(emoji.demojize(message.text))
        self.bot.send_message(
            message.chat.id, message.text,
            reply_markup=keyboards.main)


if __name__ == '__main__':
    logger.info('Bot started')
    bot = Bot()
    bot.run()
