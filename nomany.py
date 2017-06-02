import sqlite3

def check_many(minimal_coin):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    #получаем сумму из открытого счета
    coin_children_open = c.execute("SELECT number_open FROM children")
    coins_open = int(coin_children_open)
    #проверка
    if coins_open < minimal_coin:
        return("Ooops, just look children have not many to needs_coin")

if __name__ == "__main__":
    print(check_many(minimal_coin))
