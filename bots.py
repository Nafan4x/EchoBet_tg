import data
from telebot import types
def add_bot(call, bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item3 = types.InlineKeyboardButton("<Назад", callback_data='BACK_PROFILE_CALLBACK')
    markup.add(item3)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Введите название бота', reply_markup=item3)
    data.update_actions(call.message.chat.id, 'NAME INSERT')



    #бд для общения с ботом


