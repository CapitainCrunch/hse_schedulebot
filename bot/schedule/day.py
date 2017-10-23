from datetime import datetime

from bot.logger import log
from bot.models import Lessons, Users
from bot.service.common_handlers import send_cancel, start
from bot.utils.functions import is_cancelled, typing
from bot.utils.keyboards import BACK_KEY, SCHEDULE_KEYBOARD, START_KEYBOARD
from bot.utils.messages import MESSAGES
from bot.utils.schema import DAY_MAPPING
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.bot import Bot
from telegram.ext import CommandHandler, ConversationHandler, RegexHandler
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update

MESSAGES = MESSAGES['schedule:day']


@log
@typing
def on_day(bot: Bot, update: Update, next_day: bool=False) -> int:
    uid = update.message.from_user.id
    chat_id = update.message.chat.id
    message = update.message.text
    if is_cancelled(message):
        return send_cancel(bot, uid)

    lessons = Lessons.select().join(Users).where(
        Users.telegram_id == uid).get()
    send_params = {
        'chat_id': chat_id,
        'parse_mode': ParseMode.MARKDOWN
    }
    schedule = dict(zip(DAY_MAPPING, [lessons.monday, lessons.tuesday,
                                      lessons.wednesday, lessons.thursday,
                                      lessons.friday, lessons.saturday]))
    day = (datetime.now().weekday() + int(next_day)) % 7
    try:
        bot.send_message(text=schedule[DAY_MAPPING[day]], **send_params)
    except IndexError:
        bot.send_message(text=MESSAGES['on_day:sunday'], **send_params)
    return ConversationHandler.END


@log
@typing
def on_tomorrow(bot: Bot, update: Update) -> None:
    return on_day(bot, update, next_day=True)


def register(dispatcher: Dispatcher) -> None:
    day_schedule = ConversationHandler(
        entry_points=[RegexHandler(SCHEDULE_KEYBOARD[0][0], on_day),
                      RegexHandler(SCHEDULE_KEYBOARD[0][1], on_tomorrow)],
        states={},  # is it correct?
        fallbacks=[CommandHandler('start', start)]
    )
    dispatcher.add_handler(day_schedule)
