import telebot
from telebot import custom_filters
import os
from loguru import logger
from src.utils.io import write_json, read_file
from src.constants import keyboards, keys, states
import emoji
from src.bot import bot
from filters import IsAdmin
from src.db import db
from src.data import DATA_DIR
from utils.keyboard import create_keyboard
from user import User


class Bot:
    """
    Telegram bot 
    """
    def __init__(self, telebot, mongodb):
        self.bot = telebot
        self.db = mongodb

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())
        self.bot.add_custom_filter(custom_filters.TextMatchFilter())
        self.bot.add_custom_filter(custom_filters.TextStartsFilter())

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
                f"Hi <strong>{message.chat.first_name}</strong>!",
                reply_markup=keyboards.main
            )

            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(text=[keys.ask_question])
        def ask_question(message):
            self.update_state(message.chat.id, states.ask_question)

            self.send_message(
                message.chat.id,
                read_file(DATA_DIR / 'guide.html'),
                reply_markup=create_keyboard(keys.cancel, keys.send_question)
            )

        @self.bot.message_handler(text=[keys.cancel])
        def cancel(message):
            user = User(chat_id=message.chat.id)
            user.reset()
            self.update_state(message.chat.id, states.main)

            self.send_message(
                message.chat.id,
                'cancelled!',
                reply_markup=keyboards.main
            )

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            # print("i am in echo")
            user = User(chat_id=message.chat.id)
            if user.state == states.ask_question:
                self.db.users.update_one(
                    {'chat.id': message.chat.id},
                    {'$push': {'current_question': message.text}},
                )
                print(db.users.find_one({'chat.id': message.chat.id}).get('current_question'))

                self.send_message(
                    message.chat.id, 
                    user.current_question(),
                )
        
    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(chat_id, emoji.emojize(text), reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        self.db.users.update_one(
            {'chat_id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    logger.info('Bot started')
    bot = Bot(telebot=bot, mongodb=db)
    bot.run()
