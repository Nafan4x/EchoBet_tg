import config
import telebot
import profile
import random

from telebot import types
bot = telebot.TeleBot(config.TOKEN)

print("start")


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💼 Профиль")
    item5 = types.KeyboardButton("🤖 Мои боты")
    markup.add(item1, item5)
    bot.send_message(message.chat.id,
        "Добро пожаловать, воспользуйтесь кнопками для навигации",
        parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def chater(message):
    chatid = str(message.chat.id)
    if message.chat.type == 'private':
        profile.show_profile(chatid, bot)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chatid = str(call.message.chat.id)
    try:
        if call.data == 'ADD_BOT_CALLBACK':
            profile.add_bot(call,bot)
        if call.data == 'BACK_PROFILE_CALLBACK':
            profile.back_profile(call,bot)
    except Exception as ex:
        print(ex)



bot.infinity_polling()
