import telegram
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from pytz import timezone

import datetime as dt
import random

token = "5614139151:AAFma3nOc-DwmnuhFvRRxtOmSYn0tufuFAg"
bot = telegram.Bot(token=token)

updater = Updater(token,
                  use_context=True)

j = updater.job_queue

register_cmd = "Зарегистрироваться \U0001F385"
unregister_cmd = "Отменить регистрацию \U0001F44E"
show_participators_cmd = "Показать участников"
help_cmd = "Помощь \U00002753"

my_tz = timezone('Etc/GMT-7')
send_time = dt.datetime(2022, 10, 24, 16, 52, 0, 000000, tzinfo=my_tz)

buttons = [[KeyboardButton(register_cmd), KeyboardButton(unregister_cmd)], 
    [KeyboardButton(help_cmd), KeyboardButton(show_participators_cmd)]]

#users = [(1, 'ALEX', 'ALEX_NICK22222212'), (2, 'TOM', 'TOM_NICK22222212'), (3, 'JIM', 'JIM_NICK22222212'), (4, 'SARA', 'SARA_NICK22222212')]
users = []

def id_list_debug():
    print(f"current id list:\n {users}" )

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Для участия в Тайном Санте от тебя требуется лишь нажать кнопку 'Зарегистрироваться'. В свое время тебе придет имя человека, который будет ждать от тебя подарок",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))

def generate(context: CallbackContext):
    #print("generation begins")
    random.shuffle(users)
    #id_list_debug()

    for i in range(-1, len(users) - 1):
        user_id = users[i][0]
        santa_name = users[i][1]
        name = users[i+1][1]
        nickname = users[i+1][2]
        message = f"{santa_name}, ты даришь подарок этому прекрасному человеку: \n{name} (@{nickname})"
        #print(message)
        try:
            context.bot.send_message(chat_id=user_id, text=message)
            break
        except Exception as e:
            print(e)

def message_handler(update: Update, context: CallbackContext):
    user_info = (update.message.chat_id, str(update.message.from_user.first_name), str(update.message.from_user.username))

    if update.message.text == register_cmd:
        if user_info not in users:
            users.append(user_info)
            update.message.reply_text("Ты в игре \U0001F60E")
        else:
            update.message.reply_text("Ты уже зарегистрирован")
        #id_list_debug()

    elif update.message.text == unregister_cmd:
        if user_info in users:
            users.remove((update.message.chat_id, str(update.message.from_user.first_name), str(update.message.from_user.username)))
            update.message.reply_text("Ты убран из списков участников. Если передумаешь, жми 'Зарегистрироваться'")
        else:
            update.message.reply_text("Ты не зарегистрирован")
        #id_list_debug()

    elif update.message.text == show_participators_cmd:
        for user in users:
            update.message.reply_text(f"@{user[2]}")

    elif update.message.text == help_cmd:
        update.message.reply_text(
            "Чтобы принять участие в Тайном Санте, тебе нужно нажать кнопку 'Зарегистрироваться'. В любой момент ты можешь выйти из игры кнопкой 'Отменить регистрацию'",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))

    else:
        update.message.reply_text(
            "Прости, я не понимаю текст. Пользуйся кнопками, плз", 
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  

updater.start_polling()
j.run_once(generate, send_time)