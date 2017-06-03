import telebot
import sqlite3
from transaction import transaction
from get_balance import balance_child, balance_parent
from create_task import _task

bot = telebot.TeleBot('334091792:AAExM2izWSclqPoHZ109hrsZK-3cfUAVxzs')

@bot.message_handler(commands=['start'])
def start(message):
    welcome = "Hi! I'm a Finance Motivation Children bot!"
    bot.send_message(message.chat.id, welcome)

@bot.message_handler(commands=['parent_balance'])
def parents_balance(message):
    s = balance_parent("Sveta1")
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['children_balance'])
def children_balance(message):
    s = balance_child("Sveta1")
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['sent_bonus'])
def bonus_sent(message):
    row_coin = str(message.text)
    coin = str(row_coin[12::])
    if len(coin) == 0:
        bot.send_message(message.chat.id, "Enter coin!")
    else:
        transaction.bonus(coin, 'fb4a1052-070a-4723-b8ec-fea66b7a1599', '9b6316b2-7598-4d7d-a681-6e6145b391ab')
        bot.send_message(message.chat.id, "Ok! Sent to {}".format(coin))

@bot.message_handler(commands=['sent_mulctl'])
def mictf(message):
    row_coin = str(message.text)
    coin = str(row_coin[12::])
    if len(coin) == 0:
        bot.send_message(message.chat.id, "Enter coin!")
    else:
        transaction.mulctl(coin, '65476977-81e6-4b06-8842-3de38bcb6c4a')
        bot.send_message(message.chat.id, "Ok! Sent mulctl to {}".format(coin))

@bot.message_handler(commands=['sent_task'])
def task(message):
    row_task = str(message.text)
    tasks = str(row_task[10::])
    _task('64e084d3-2787-4782-91b1-cbb82cee6560', '{}'.format(tasks), 10)
    bot.send_message(message.chat.id, "Create task:%s" % tasks)

if __name__=='__main__':
        bot.polling(none_stop=True)
