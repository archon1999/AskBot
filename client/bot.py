from telebot import TeleBot, types

import config

from backend.models import BotUser

bot = TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    chat_id = message.chat.id
    BotUser.objects.get_or_create(chat_id=chat_id)
    text = '<b>Добро пожаловать в бот</b>\n'
    text += 'Укажите часовой пояс(введите число от -12 до +12)\n'
    text += 'Например, для города Москва это +3'
    bot.send_message(chat_id, text)


@bot.message_handler(func=lambda message: message.text == 'Хорошо')
def ok_message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if not user.ok:
        user.ok = True
        user.save()
        bot.send_message(chat_id, '👍👍',
                         reply_markup=types.ReplyKeyboardRemove(),
                         timeout=30)


@bot.message_handler()
def message_handler(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    if user.offset is None:
        try:
            user.offset = int(message.text)
            assert(-12 <= user.offset <= 12)
        except Exception:
            bot.send_message(chat_id, 'Введите корректное значение!',
                             timeout=30)
        else:
            user.save()
            bot.send_message(chat_id, 'Сохранено!',
                             timeout=30)


if __name__ == "__main__":
    print(bot.get_me())
    # bot.polling()
    bot.infinity_polling()
