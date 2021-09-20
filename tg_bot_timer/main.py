import ptbot
from pytimeparse import parse
import os
import random

TG_TOKEN = os.environ["TG_TOKEN"]  
TG_CHAT_ID = '557228766'
bot = ptbot.Bot(TG_TOKEN)
bot.send_message(TG_CHAT_ID, "Привет! Задай время")

def reply(chat_id, text):
    parse_text = parse(text)
    message_id = bot.send_message(chat_id, "Осталось {} секунд!".format(parse(text)))
    bot.create_countdown(parse(text), notify, chat_id=chat_id, message_id=message_id, secs_in_meesage=parse_text)
    bot.create_timer(parse(text), time_up, chat_id=chat_id)


def notify(secs_left, chat_id, message_id, secs_in_message):
    bot.update_message(chat_id, message_id, "Осталось {} секунд!\n {}".format(secs_left, render_progressbar(secs_in_message, secs_in_message - secs_left)))

def time_up(chat_id):
    bot.send_message(chat_id, "Время вышло!")

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

bot.reply_on_message(reply)
bot.run_bot()