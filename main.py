import config
import telebot
import profile
import random
from data import *
import bots
import json

from telebot import types
bot = telebot.TeleBot(config.TOKEN)

print("start")


def show_home(call,bot):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("💼 Профиль", callback_data='SHOW_PROFILE_CALLBACK')
    item5 = types.InlineKeyboardButton("🤖 Мои боты", callback_data='SHOW_BOT_LIST_CALLBACK')
    item2 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    markup.add(item1, item5).row(item2)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                     "Добро пожаловать в EchoTrade, здесь вы можете купить ботов для трейдинга, а также пользоваться ботами без комиссии. Используйте кнопки ниже для навигации",
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("💼 Профиль", callback_data='SHOW_PROFILE_CALLBACK')
    item5 = types.InlineKeyboardButton("🤖 Мои боты", callback_data='SHOW_BOT_LIST_CALLBACK')
    item2 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    markup.add(item1, item5).row(item2)
    bot.send_message(message.chat.id,
        "Добро пожаловать в EchoTrade!\n"
        "Здесь вы можете купить ботов для трейдинга, а также пользоваться ботами без комиссии.\n"
        "Используйте кнопки ниже для навигации",
        parse_mode='html', reply_markup=markup)
    print(read_table('chats'))

    table1 = [i['chat_id'] for i in read_table('chats')]
    table2 = [i['chat_id'] for i in read_table('tg_actions')]

    if not(message.chat.id in table1 or message.chat.id in table2):
        create_chats(chat_id=message.chat.id, username="{0.username}".format(
            message.from_user), balance=0)
        create_actions(chat_id=message.chat.id, action='none')


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
            bots.add_bot(call,bot)
        if call.data == 'SHOW_PROFILE_CALLBACK':
            profile.show_profile(call, bot)

        #Кнопки назад
        if call.data == 'BACK_HOME_CALLBACK':
            show_home(call,bot)

    except Exception as ex:
        print(ex)



bot.infinity_polling()
