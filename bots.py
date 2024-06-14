import data
from telebot import types

def add_bot(call, bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item3 = types.InlineKeyboardButton("<Назад", callback_data='BACK_PROFILE_CALLBACK')
    markup.add(item3)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Введите название бота', reply_markup=item3)
    data.update_actions(call.message.chat.id, 'BOT_NAME_INSERT')

def add_api(call,bot):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Ввести Base-key", callback_data='INSERT_BASE_API')
    item2 = types.InlineKeyboardButton("Ввести Secret-key", callback_data='INSERT_SECRET_API')
    item3 = types.InlineKeyboardButton("Ввести Название", callback_data='INSERT_NAME_API')
    item4 = types.InlineKeyboardButton("Ввести Биржу", callback_data='INSERT_BOURSE_API')
    item5 = types.InlineKeyboardButton("✅Сохранить", callback_data='SAVE_API')
    item6 = types.InlineKeyboardButton("❌Отмена", callback_data='CANSEL_ADD_API')
    markup.add(item1).row(item2).row(item3).row(item4).row(item5, item6)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Это меню для добавления API в ваш аккаунт\n'
                               'Введите все поля и нажмите кнопку "✅Сохранить"', reply_markup=markup)
    data.create_keys(chat_id=call.message.chat.id)

def send_add_api(call,bot):

    values = data.get_editable_keys(chat_id=call)
    print(values)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(f"Ввести Base-key ({values['base_key']})", callback_data='INSERT_BASE_API')
    item2 = types.InlineKeyboardButton(f"Ввести Secret-key ({values['secret_key']})", callback_data='INSERT_SECRET_API')
    item3 = types.InlineKeyboardButton(f"Ввести Название ({values['key_name']})", callback_data='INSERT_NAME_API')
    item4 = types.InlineKeyboardButton(f"Ввести Биржу ({values['bourse']})", callback_data='INSERT_BOURSE_API')
    item5 = types.InlineKeyboardButton("✅Сохранить", callback_data='SAVE_API')
    item6 = types.InlineKeyboardButton("❌Отмена", callback_data='CANSEL_ADD_API')
    markup.add(item1).row(item2).row(item3).row(item4).row(item5, item6)

    bot.send_message(chat_id=call,
                          text='Это меню для добавления API в ваш аккаунт\n'
                               f'Введите все поля и нажмите кнопку "✅Сохранить"', reply_markup=markup)

def error_add_api(call, bot):
    values = data.get_editable_keys(chat_id=call.message.chat.id)
    #print(values)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(f"Ввести Base-key ({values['base_key']})", callback_data='INSERT_BASE_API')
    item2 = types.InlineKeyboardButton(f"Ввести Secret-key ({values['secret_key']})",
                                       callback_data='INSERT_SECRET_API')
    item3 = types.InlineKeyboardButton(f"Ввести Название ({values['key_name']})", callback_data='INSERT_NAME_API')
    item4 = types.InlineKeyboardButton(f"Ввести Биржу ({values['bourse']})", callback_data='INSERT_BOURSE_API')
    item5 = types.InlineKeyboardButton("✅Сохранить", callback_data='SAVE_API')
    item6 = types.InlineKeyboardButton("❌Отмена", callback_data='CANSEL_ADD_API')
    markup.add(item1).row(item2).row(item3).row(item4).row(item5, item6)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                     text='Это меню для добавления API в ваш аккаунт\n'
                          f'Введите все поля и нажмите кнопку "✅Сохранить"\n🔴Ошибка: Все поля должны быть заполнены', reply_markup=markup)






    # data.update_actions(call.message.chat.id, 'API_NAME_INSERT')
    #
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item3 = types.InlineKeyboardButton("❌Отмена", callback_data='CANSEL_ADD_API')
    # markup.add(item3)
    # bot.send_message(chat_id=call.message.chat.id,
    #                  text='Введите Base-key Api', reply_markup=markup)




