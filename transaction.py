import sqlite3

class transaction():

    #нужды
    def to_needs(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT balance_parent FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        if coin_transaction_from_parents < 0:
            return("No many")
        else:
            c.execute("UPDATE parents SET balance_parent='{}'".format(coin_transaction_from_parents))
            #Получаем сумму на счету ребенка
            coin_children_all = c.execute("SELECT balance_needs FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_all[0]:
                coin_children_all = i
            #зачисляем ему на счет сумму
            coin_transaction_to_children = int(coin_children_all) + int(coin)
            c.execute("UPDATE parents SET balance_needs='{}'".format(coin_transaction_to_children))
            conn.commit()
            conn.close()

    #в закрытый
    def to_close(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT balance_parent FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        if coin_transaction_from_parents < 0:
            return("No many")
        else:
            c.execute("UPDATE parents SET balance_parent='{}'".format(coin_transaction_from_parents))
            #Получаем сумму на закрытом счету ребенка
            coin_children_close = c.execute("SELECT balance_close FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_close[0]:
                coin_children_close = i
            #зачисляем ему на закрытый счет сумму
            coin_transaction_to_children = int(coin_children_close) + int(coin)
            c.execute("UPDATE parents SET balance_close='{}'".format(coin_transaction_to_children))
            conn.commit()
            conn.close()

    #закрытый-открытый
    def in_close_to_open(coin, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем сумму из закрытого счета ребенка
        coin_children_close = c.execute("SELECT balance_close FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_close[0]:
            coin_children_close = i
        if coin_children_close < 0:
            return("No many")
        else:
            #получаем сумму из открытого счета
            coin_children_open = c.execute("SELECT balance_open FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_open[0]:
                coin_children_open = i
            #Списываем сумму с закрытого
            coin_transaction_from_close = int(coin_children_close) - int(coin)
            c.execute("UPDATE parents SET balance_close='{}'".format(coin_transaction_from_close))
            #Записываем на открытый счет
            coin_transaction_to_open = int(coin_children_open) + int(coin)
            c.execute("UPDATE parents SET balance_open='{}'".format(coin_transaction_to_open))
            conn.commit()
            conn.close()

    def bonus(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_parents_all = c.execute("SELECT balance_parent FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        if coin_transaction_from_parents < 0:
            return("No many")
        else:
            c.execute("UPDATE parents SET balance_parent='{}'".format(coin_transaction_from_parents))
            #получаем сумму из открытого счета ребенка
            coin_children_open = c.execute("SELECT balance_open FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_open[0]:
                coin_children_open = i
            #Записываем на открытый счет
            coin_transaction_to_open = int(coin_children_open) + int(coin)
            c.execute("UPDATE parents SET balance_open='{}'".format(coin_transaction_to_open))
            conn.commit()
            conn.close()

    def mulctl(coin, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_children_open = c.execute("SELECT balance_open FROM parents WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_open[0]:
            coin_children_open = i
        coin_transaction_to_open = int(coin_children_open) - int(coin)
        if coin_transaction_to_open < 0:
            return("No many")
        else:
            c.execute("UPDATE parents SET balance_open='{}'".format(coin_transaction_to_open))
            conn.commit()
            conn.close()

#transaction.in_close_to_open(10, "65476977-81e6-4b06-8842-3de38bcb6c4a")
#transaction.to_needs(10, 'fb4a1052-070a-4723-b8ec-fea66b7a1599', '9b6316b2-7598-4d7d-a681-6e6145b391ab')
#transaction.in_close_to_open(20, '9b6316b2-7598-4d7d-a681-6e6145b391ab')
#transaction.to_close(10, 'fb4a1052-070a-4723-b8ec-fea66b7a1599', '9b6316b2-7598-4d7d-a681-6e6145b391ab')
#transaction.bonus(10, '64e084d3-2787-4782-91b1-cbb82cee6560', '65476977-81e6-4b06-8842-3de38bcb6c4a')
#transaction.mulctl(10, '9b6316b2-7598-4d7d-a681-6e6145b391ab')
