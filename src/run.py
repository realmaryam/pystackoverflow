import telebot
import os
from loguru import logger
from src.utils.io import write_json
from src.constants import keyboards, keys, states
import emoji
from src.bot import bot
from filters import IsAdmin
from src.db import db


class Bot:
    """
    Telegram bot to randomly connect people to talk
    """
    def __init__(self, telebot, mongodb):
        self.bot = telebot
        self.db = mongodb

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.send_message(
                message.chat.id, 
                f"Hey <strong>{message.chat.first_name}</strong>!",
                reply_markup=keyboards.main
            )

        @self.bot.message_handler(text=[keys.settings])
        def exit(message):
            pass

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            self.send_message(
                message.cgat.id, message.text,
                reply_markup=keyboards.main
            )
        
    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        self.db.users.update_one(
            {'chat_id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    logger.info('Bot started')
    bot = Bot(telebot=bot, mongodb=db)
    bot.run()
