import telebot

bot = telebot.TeleBot('8872813048:AAG8RHjfBZl_VSnoub4UGRo-GJPO0w8PKvE')
tasks = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот - список дел.\nКоманды: /add текст, /list, /delete номер')

@bot.message_handler(commands=["add"])
def add_task(message):
    chat_id = message.chat.id
    text = message.text.replace('/add', '').strip()

    if chat_id not in tasks:
        tasks[chat_id] = []

    if text == '':
        bot.send_message(chat_id, 'Напиши задачу после команды. Пример: /add купить хлеб')
    else:
        tasks[chat_id].append(text)
        bot.send_message(chat_id, 'Задача добавлена: ' + text)

@bot.message_handler(commands=["list"])
def list_tasks(message):
    chat_id = message.chat.id
    if chat_id not in tasks or len(tasks[chat_id]) == 0:
        bot.send_message(chat_id, 'Список дел пуст')
    else:
        text = 'Твои задачи:\n'
        for i in range(len(tasks[chat_id])):
            text += str(i + 1) + '. ' + tasks[chat_id][i] + '\n'
        bot.send_message(chat_id, text)

@bot.message_handler(commands=["delete"])
def delete_task(message):
    chat_id = message.chat.id
    number = message.text.replace('/delete', '').strip()

    if chat_id not in tasks or len(tasks[chat_id]) == 0:
        bot.send_message(chat_id, 'Список дел пуст')
    elif not number.isdigit():
        bot.send_message(chat_id, 'Укажи номер задачи. Пример: /delete 1')
    else:
        index = int(number) - 1
        if index < 0 or index >= len(tasks[chat_id]):
            bot.send_message(chat_id, 'Нет задачи с таким номером')
        else:
            removed = tasks[chat_id].pop(index)
            bot.send_message(chat_id, 'Задача удалена: ' + removed)

bot.polling(none_stop=True, interval=0)