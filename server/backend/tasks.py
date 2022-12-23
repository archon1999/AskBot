import os
import random
import traceback

import dotenv
import telebot
from telebot import types
from django.utils import timezone

from backend.models import EntityTime, BotUser


dotenv.load_dotenv('../.env')
TOKEN = os.getenv('BOT_TOKEN')


def entity_process(entity_time_id, offset):
    entity_time = EntityTime.objects.get(id=entity_time_id)
    if not entity_time.get_prev() and timezone.now().weekday() == 6:
        return

    entity = entity_time.entity
    text_list = []
    for entity_text in entity.texts.all():
        text_list.append(entity_text.get_text())

    text = random.choice(text_list)
    users = BotUser.objects.filter(offset=offset)
    prev_entity_time = entity_time.get_prev()
    if prev_entity_time:
        users = users.filter(ok=True)

    bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
    for user in users:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Хорошо')
        user.ok = False
        user.save()
        try:
            bot.send_message(user.chat_id, text,
                             reply_markup=keyboard,
                             timeout=30)
        except Exception:
            traceback.print_exc()
