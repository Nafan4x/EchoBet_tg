def add_bot(call, bot):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Введи API token ByBit')
    #бд для общения с ботом