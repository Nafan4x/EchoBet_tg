import data
from telebot import types

def add_bot(call, bot):
    api_keys = None
    try:
        api_keys = data.get_editable_keys(chat_id=call.message.chat.id)
    except:
        pass
    all_keys = data.read_table("keys")
    user_keys = []
    for i in all_keys:
        for j in i:
            if i[j] == call.message.chat.id:
                user_keys.append(i)


    if api_keys is None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        item3 = types.InlineKeyboardButton("<Назад", callback_data='BACK_HOME_CALLBACK')
        markup.add(item3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='У вас нет API ключа. Добавьте его и вернитесь на эту страницу', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        key_names = []
        for i in user_keys:
           key_names.append(types.InlineKeyboardButton(f"{i['key_name']}", callback_data=f"{i['key_id']}"))

        f = 0
        for i in range(0, len(key_names) - 1, 2):
            if len(key_names) % 2 == 0:
                markup.add(key_names[i], key_names[i + 1], row_width=2)

            else:
                markup.add(key_names[i], key_names[i + 1], row_width=2)
                f = 1
        if f == 1:
            markup.add(key_names[len(key_names) - 1])
        if len(key_names) == 1:
            markup.add(key_names[0], row_width=1)
        item3 = types.InlineKeyboardButton("<Назад", callback_data='BACK_HOME_CALLBACK')
        markup.row(item3)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='⬇️⬇️⬇️  Выберите API ключ для бота  ⬇️⬇️⬇️', reply_markup=markup)
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

if __name__ == "__main__":
    all_keys = data.read_table("keys")
    print(all_keys)
    user_keys = []
    for i in all_keys:
        for j in i:
            if i[j] == 841051288:
                user_keys.append(i['key_id'])
    print(user_keys)

