import telebot
from telebot import types

def show_profile(chatid, bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Профиль", callback_data='PROFILE_CALLBACK')
    item2 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    markup.add(item1, item2)
    bot.send_message(chatid, "Ваш уникальный ID: " + chatid, reply_markup=markup)


def add_bot(call, bot):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Введи API token ByBit')
    #бд для общения с ботом



def add_bot1(call, bot):

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Профиль", callback_data='PROFILE_CALLBACK')
    item2 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    item3 = types.InlineKeyboardButton("<Назад", callback_data='BACK_PROFILE_CALLBACK')
    markup.add(item1, item2, item3)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты нажал на кнопку 1',reply_markup=markup)

def back_profile(call,bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Профиль", callback_data='PROFILE_CALLBACK')
    item2 = types.InlineKeyboardButton("➕ Добавить бота", callback_data='ADD_BOT_CALLBACK')
    markup.add(item1, item2)
    bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Ваш уникальный ID: " + str(call.message.chat.id), reply_markup=markup)




