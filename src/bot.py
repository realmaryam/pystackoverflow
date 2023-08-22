import os
import telebot
from telebot import apihelper


apihelper.ENABLE_MIDDLEWARE = True

# Initialize bot
bot = telebot.TeleBot(
    os.environ['BOT_TOKEN'], parse_mode='HTML'
)