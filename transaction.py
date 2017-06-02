import sqlite3

class transaction():

    #нужды
    def to_needs(coin):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT number_parents FROM parents")
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("INSERT INTO parents (number_parents) VALUES ({})".format(coin_transaction_from_parents))
        #Получаем сумму на счету ребенка
        coin_children_all = c.execute("SELECT number_needs FROM children")
        #зачисляем ему на счет сумму
        coin_transaction_to_children = int(coin_children_all) + int(coin)
        c.execute("INSERT INTO children (number_needs) VALUES ({})".format(coin_transaction_to_children))
        conn.commit()
        conn.close()

    #в закрытый
    def to_close(coin):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT number_parents FROM parents")
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("INSERT INTO parents (number_parents) VALUES ({})".format(coin_transaction_from_parents))
        #Получаем сумму на закрытом счету ребенка
        coin_children_close = c.execute("SELECT number_close FROM children")
        #зачисляем ему на закрытый счет сумму
        coin_transaction_to_children = int(coin_children_close) + int(coin)
        c.execute("INSERT INTO children (number_close) VALUES ({})".format(coin_transaction_to_children))
        conn.commit()
        conn.close()

    #закрытый-открытый
    def to_close_to_open(coin):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем сумму из закрытого счета ребенка
        coin_children_close = c.execute("SELECT number_close FROM children")
        #получаем сумму из открытого счета
        coin_children_open = c.execute("SELECT number_open FROM children")
        #Списываем сумму с закрытого
        coin_transaction_from_close = int(coin_children_close) - int(coin)
        c.execute("INSERT INTO children (number_close) VALUES ({})".format(coin_transaction_from_close))
        #Записываем на открытый счет
        coin_transaction_to_open = int(coin_children_open) + int(coin)
        c.execute("INSERT INTO children (number_open) VALUES ({})".format(coin_transaction_to_open))
        conn.commit()
        conn.close()

    def bonus(coin):
        conn = sqlite3.connect('database')
        c = conn.cursor()
        coin_parents_all = c.execute("SELECT number_parents FROM parents")
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("INSERT INTO parents (number_parents) VALUES ({})".format(coin_transaction_from_parents))
        #получаем сумму из открытого счета ребенка
        coin_children_open = c.execute("SELECT number_open FROM children")
        #Записываем на открытый счет
        coin_transaction_to_open = int(coin_children_open) + int(coin)
        c.execute("INSERT INTO children (number_open) VALUES ({})".format(coin_transaction_to_open))
        conn.commit()
        conn.close()        
