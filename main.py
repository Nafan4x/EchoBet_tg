import config
import telebot

import data
import profile
import random
from data import *
import bots
import json

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

print("start")


def show_home(call, bot):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("💼 Профиль", callback_data='SHOW_PROFILE_CALLBACK')
    item2 = types.InlineKeyboardButton("🤖 Мои боты", callback_data='SHOW_BOT_LIST_CALLBACK')
    item3 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    item4 = types.InlineKeyboardButton("➕ Добавить API-key", callback_data='ADD_API_CALLBACK')
    markup.add(item1, item2).row(item3, item4)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
    "Добро пожаловать в EchoTrade, здесь вы можете купить ботов для трейдинга, а также пользоваться ботами без комиссии. Используйте кнопки ниже для навигации",
                          parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("💼 Профиль", callback_data='SHOW_PROFILE_CALLBACK')
    item2 = types.InlineKeyboardButton("🤖 Мои боты", callback_data='SHOW_BOT_LIST_CALLBACK')
    item3 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    item4 = types.InlineKeyboardButton("➕ Добавить API-key", callback_data='ADD_API_CALLBACK')
    markup.add(item1, item2).row(item3, item4)
    bot.send_message(message.chat.id,
                     "Добро пожаловать в EchoTrade!\n"
                     "Здесь вы можете купить ботов для трейдинга, а также пользоваться ботами без комиссии.\n"
                     "Используйте кнопки ниже для навигации",
                     parse_mode='html', reply_markup=markup)
    print(read_table('chats'))

    in_table1 = message.chat.id in [i['chat_id'] for i in read_table('chats')]
    in_table2 = message.chat.id in [i['chat_id'] for i in read_table('tg_actions')]

    if not (in_table1 or in_table2):
        create_chats(chat_id=message.chat.id, username="{0.username}".format(
            message.from_user), balance=0)
        create_actions(chat_id=message.chat.id, action='none')


@bot.message_handler(content_types=['text'])
def chater(message):
    chatid = message.chat.id
    if message.chat.type == 'private':
        #ADD API
        if get_actions(chat_id=chatid) == "INSERT_BASE_API":
            data.update_keys(key_id=get_editable_keys(chatid)['key_id'], base_key=str(message.text))
            data.update_actions(message.chat.id, 'none')
            #bot.send_message(chat_id=chatid, text=f'✅base-key = {message.text}')
            bots.send_add_api(call=chatid,bot=bot)

        if get_actions(chat_id=chatid) == "INSERT_SECRET_API":
            data.update_keys(key_id=get_editable_keys(chatid)['key_id'], secret_key=str(message.text))
            data.update_actions(message.chat.id, 'none')
            #bot.send_message(chat_id=chatid, text=f'✅secret-key = {message.text}')
            bots.send_add_api(call=chatid, bot=bot)

        if get_actions(chat_id=chatid) == "INSERT_NAME_API":
            data.update_keys(key_id=get_editable_keys(chatid)['key_id'], key_name=str(message.text))
            data.update_actions(message.chat.id, 'none')
            #bot.send_message(chat_id=chatid, text=f'✅name = {message.text}')
            bots.send_add_api(call=chatid, bot=bot)

        if get_actions(chat_id=chatid) == "INSERT_BOURSE_API":
            data.update_keys(key_id=get_editable_keys(chatid)['key_id'], bourse=str(message.text))
            data.update_actions(message.chat.id, 'none')
            #bot.send_message(chat_id=chatid, text=f'✅bourse = {message.text}')
            bots.send_add_api(call=chatid, bot=bot)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chatid = str(call.message.chat.id)
    try:
        if call.data == 'ADD_BOT_CALLBACK':
            bots.add_bot(call, bot)
        if call.data == 'SHOW_PROFILE_CALLBACK':
            profile.show_profile(call, bot)
        if call.data == 'ADD_API_CALLBACK':
            bots.add_api(call,bot)
        # Кнопки назад
        if call.data == 'BACK_HOME_CALLBACK':
            show_home(call, bot)
        #Кнопки отмены добавления
        if call.data == "CANSEL_ADD_API":
            pass

        #ADD BOTS
        

        #ADD API
        if call.data == 'INSERT_BASE_API':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите base-key")
            #bot.send_message(chat_id=chatid, text="Введите base-key")
            data.update_actions(chatid, "INSERT_BASE_API")

        if call.data == 'INSERT_SECRET_API':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите Secret-key")
            #bot.send_message(chat_id=chatid, text="Введите Secret-key")
            data.update_actions(chatid, "INSERT_SECRET_API")

        if call.data == 'INSERT_NAME_API':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите название")
            #bot.send_message(chat_id=chatid, text="Введите название")
            data.update_actions(chatid, "INSERT_NAME_API")

        if call.data == 'INSERT_BOURSE_API':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введите биржу")
            #bot.send_message(chat_id=chatid, text="Введите биржу")
            data.update_actions(chatid, "INSERT_BOURSE_API")

        if call.data == 'SAVE_API':
            values = data.get_editable_keys(chat_id=call.message.chat.id)
            for i in values:
                print(i)
                if values[i] is None:
                    bots.error_add_api(call,bot)
                    return
            show_home(call, bot)

        if call.data == 'CANSEL_ADD_API':
            data.delete_record('keys', data.get_editable_keys(chat_id=call.message.chat.id)['key_id'])
            show_home(call, bot)

    except Exception as ex:
        print(ex)


bot.infinity_polling()
