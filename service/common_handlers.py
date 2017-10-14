import emoji
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

from utils.keyboards import start_keyboard
from models import Users
from logger import log


# TODO: add decorator, which asks for corp email

@log
def start(bot, update):
    uid = update.message.from_user.id
    winking_face = emoji.emojize(':winking_face:')
    msg = f'Привет! У меня можно подсмотреть расписания ' \
          f'электричек или твоей учебы{winking_face}'
    bot.send_message(
        uid,
        msg,
        reply_markup=ReplyKeyboardMarkup(start_keyboard)
    )


def register(dp):
    dp.add_handler(CommandHandler('start', start))