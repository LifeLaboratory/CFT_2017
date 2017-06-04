import telebot
import sqlite3
from transaction import transaction
from get_balance import balance_child, balance_parent
from create_task import create_task
from done_task import not_executed, executed, close_task_user, _all

bot = telebot.TeleBot('334091792:AAExM2izWSclqPoHZ109hrsZK-3cfUAVxzs')

id_parent_g = None
id_child = None

try:
    @bot.message_handler(commands=['start'])
    def start(message):
        welcome = """Hi! I'm a Finance Motivation Children bot!
Type /help to get a more info"""
        bot.send_message(message.chat.id, welcome)

    @bot.message_handler(commands=['help'])
    def help(message):
        helps = '''
Commands list:
parent_bal - balance in parents account
child_bal - balance in children account
all_t - views all task
not_exec_t - views not executable task
exec_t - views executable task
check_t - check and display the performance of the task (commands <task>)
sent_t - send moneys to children in needs score invoices (commands <coins>)
sent_m - send mulct for open invoices children (commands <coins>)
sent_bon - send bonus in open invoices children (commands <coins>)
        '''
        bot.send_message(message.chat.id, helps)

    @bot.message_handler(commands=['login'])
    def login(message):
        row = str(message.text)
        s = str(row[7::])
        if len(s) == 0:
            bot.send_message(message.chat.id, "Wrong!")
        else:
            login = str(s[:s.find(' ')])
            password = str(s[:s.find(' ')])
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT id_parent FROM parents WHERE login='{0}' and password='{1}'".format(login, password))
            global id_parent_g
            _id_parent_ = c.fetchall()
            id_parent_g = _id_parent_[0][0]
            print(id_parent_g)
            c.execute("SELECT id_child FROM children WHERE id_parent='{}'".format(id_parent_g))
            _id_child_ = c.fetchall()
            global id_child
            id_child = _id_child_[0][0]
            print(id_child)
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Authentication successful")
            return (id_parent_g, id_child)
            bot.send_message(message.chat.id, "Somewhere wrong!")

    @bot.message_handler(commands=['parent_bal'])
    def parents_balance(message):
        id_parent = id_parent_g
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            s = balance_parent(id_parent)
            bot.send_message(message.chat.id, s)

    @bot.message_handler(commands=['child_bal'])
    def children_balance(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            s = balance_child(id_c)
            bot.send_message(message.chat.id, s)

    @bot.message_handler(commands=['sent_bon'])
    def bonus_sent(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            row_coin = str(message.text)
            coin = str(row_coin[9::])
            if len(coin) == 0:
                bot.send_message(message.chat.id, "Enter coin!")
            else:
                transaction.bonus(coin, id_parent, id_c)
                messages = "Ok! Trying send to {} coin".format(coin)
                bot.send_message(message.chat.id, messages)

    @bot.message_handler(commands=['sent_n'])
    def sent_to_needs(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            if len(coin) == 0:
                bot.send_message(message.chat.id, "Enter coin!")
            else:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()
                c.execute("SELECT id_children FROM childrens WHERE id_parent='{}'".format(id_parent))
                id_children = c.fetchall()
                conn.commit()
                conn.close()
                transaction.to_needs(coin, id_parent, id_c)
                messages = "Ok! Trying send to {} coin".format(coin)
                bot.send_message(message.chat.id, messages)

    @bot.message_handler(commands=['sent_m'])
    def mictf(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            row_coin = str(message.text)
            coin = str(row_coin[7::])
            if len(coin) == 0:
                bot.send_message(message.chat.id, "Enter coin!")
            else:
                transaction.mulctl(coin, id_c)
                bot.send_message(message.chat.id, "Ok! Trying to send mulctl to {} coin".format(coin))

    @bot.message_handler(commands=['sent_t'])
    def task(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            row_task = str(message.text)
            tasks = str(row_task[7::])
            if len(tasks) == 0:
                bot.send_message(message.chat.id, "Please, sent task!")
            else:
                create_task(id_parent, id_c, '{}'.format(tasks), 10)
                bot.send_message(message.chat.id, "Create task:%s" % tasks)

    @bot.message_handler(commands=['all_t'])
    def all_task(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            s = _all(id_parent)
            print(s)
            n = 0
            for i in s:
                n += 1
                messages = "Task{0}: {1}.".format(n, i[0])
                bot.send_message(message.chat.id, messages)

    @bot.message_handler(commands=['not_exec_t'])
    def not_execute(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            s = not_executed(id_parent)
            print(s)
            n=0
            for i in s:
                n += 1
                messages = "Task{0}: {1}. Not execute".format(n, i[0])
                bot.send_message(message.chat.id, messages)

    @bot.message_handler(commands=['exec_t'])
    def execute(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            p = executed(id_parent)
            n=0
            for i in p:
                n+=1
                messages = "Task{0}: {1}. Executed".format(n, i[0])
                bot.send_message(message.chat.id, messages)

    @bot.message_handler(commands=['check_t'])
    def check(message):
        id_parent = id_parent_g
        id_c = id_child
        if id_parent == None:
            bot.send_message(message.chat.id, "Need authentication!")
        else:
            row_number = str(message.text)
            l = len(row_number)
            rowid = int(row_number[9::l])
            print(rowid)
            if len(row_number) < 0:
                bot.send_message(message.chat.id, "Wrong!")
            else:
                con = sqlite3.connect("database.db")
                c = con.cursor()
                c.execute("SELECT id_task FROM tasks WHERE status=1 and id_parent='{}'".format(id_parent))
                id_task = c.fetchall()[0][0]
                print(id_task)
                con.commit()
                con.close()
                s1 = close_task_user(id_task, id_parent, id_c)
                messages = "Task number {} was execute!".format(rowid)
                bot.send_message(message.chat.id, messages)

except:
        bot.send_message(message.chat.id, "Somewhere wrong!")

if __name__=='__main__':
    bot.polling(none_stop=True)
