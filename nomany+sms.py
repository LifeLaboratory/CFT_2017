import sqlite3
import requests

class nomany():

    def check_many(minimal_coin, number_phone):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_children_open = c.execute("SELECT balance_open FROM children").fetchall()
        for i in coin_children_open[0]:
            coin_children_open = i
        coins_open = int(coin_children_open)
        #if coins_open < minimal_coin:
            #return("Ooops, just look children have not many to needs_coin")
        message = 'Test'
        send = requests.get('http://smsc.ru/sys/send.php?login=by.sm&psw=pinlox123&phones={0}&mes={1}'.format(number_phone, message))
        return print(send)

if __name__ == '__main__':
    nomany.check_many(10, 79069700068)
