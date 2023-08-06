import telebot
import os
from loguru import logger
from src.utils.io import write_json, read_file
from src.constants import keyboards, keys, states
import emoji
from src.bot import bot
from filters import IsAdmin
from src.db import db
from src.data import DATA_DIR


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

            self.db.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )

        @self.bot.message_handler(text=[keys.ask_question])
        def ask_question(message):
            self.update_state(message.chat.id, states.ask_question)
            self.send_message(
                message.chat.id,
                read_file(DATA_DIR / 'guide.html'),
                
            )

        @self.bot.message_handler(text=[keys.cancel])
        def exit(message):
            pass

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            self.send_message(
                message.chat.id, message.text,
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
