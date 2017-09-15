import sqlite3



'''
Здесь api транзакции написанные самостоятельно подразумевающие, что у ребенка есть 3 счета
Счет нужд, с которого списываются деньги только на обязятельные нужды ребенка, описанные родителем

Закрытый счет. На нем находятся потенциальные деньги ребенка. Сначала родители делают туда перевод.
Ребенок может получить эти деньги выполняя задания. Деньги будут переходить на открытый счет.

Открытый счет. Деньги, которыми ребенок может пользоваться без ограничений.
'''

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
            c.execute("UPDATE parents SET balance_parent='{0}' WHERE id_parent='{1}'".format(coin_transaction_from_parents, id_p))
            #Получаем сумму на счету ребенка
            coin_children_all = c.execute("SELECT balance_needs FROM children WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_all[0]:
                coin_children_all = i
            #зачисляем ему на счет сумму
            coin_transaction_to_children = int(coin_children_all) + int(coin)
            c.execute("UPDATE children SET balance_needs='{0}' WHERE id_children='{1}'".format(coin_transaction_to_children, id_c))
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
            c.execute("UPDATE parents SET balance_parent='{0}' WHERE id_parent='{1}'".format(coin_transaction_from_parents, id_p))
            #Получаем сумму на закрытом счету ребенка
            coin_children_close = c.execute("SELECT balance_close FROM children WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_close[0]:
                coin_children_close = i
            #зачисляем ему на закрытый счет сумму
            coin_transaction_to_children = int(coin_children_close) + int(coin)
            c.execute("UPDATE children SET balance_close='{}'".format(coin_transaction_to_children))
            conn.commit()
            conn.close()

    #закрытый-открытый
    def in_close_to_open(coin, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем сумму из закрытого счета ребенка
        coin_children_close = c.execute("SELECT balance_close FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_close[0]:
            coin_children_close = i
        if coin_children_close < 0:
            return("No many")
        else:
            #получаем сумму из открытого счета
            coin_children_open = c.execute("SELECT balance_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_open[0]:
                coin_children_open = i
            #Списываем сумму с закрытого
            coin_transaction_from_close = int(coin_children_close) - int(coin)
            c.execute("UPDATE children SET balance_close='{}' where id_child = '{}'".format(coin_transaction_from_close, id_c))
            #Записываем на открытый счет
            coin_transaction_to_open = int(coin_children_open) + int(coin)
            c.execute("UPDATE children SET balance_open='{}' where id_child = '{}'".format(coin_transaction_to_open, id_c))
            conn.commit()
            conn.close()

    def bonus(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_parents_all = c.execute("SELECT balance_parent FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        print(coin_parents_all)
        for i in coin_parents_all[0]:
            coin_parents_all = i
        # coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        if coin_transaction_from_parents < 0:
            return ("No many")
        else:
            c.execute("UPDATE parents SET balance_parent='{}' where id_parent = '{}'".format(coin_transaction_from_parents, id_p))
            # получаем сумму из открытого счета ребенка
            coin_children_open = c.execute(
                "SELECT balance_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
            for i in coin_children_open[0]:
                coin_children_open = i
            # Записываем на открытый счет
            coin_transaction_to_open = int(coin_children_open) + int(coin)
            c.execute(
                "UPDATE children SET balance_open='{0}' WHERE id_child='{1}'".format(coin_transaction_to_open, id_c))
            conn.commit()
            conn.close()

    def mulctl(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_children = c.execute("SELECT balance_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        coin_children_open = coin_children[0]
        coin_parent = c.execute("SELECT balance_parent FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        coin_parents = coin_parent[0]
        coin_transaction_to_open = int(coin_children_open[0]) - int(coin)
        coin_transaction_to_parent = int(coin_parents[0]) + int(coin)
        if coin_transaction_to_open < 0:
            return ("No many")
        else:
            c.execute(
                "UPDATE children SET balance_open='{0}' WHERE id_child='{1}'".format(coin_transaction_to_open, id_c))
            c.execute(
                "UPDATE parents SET balance_parent='{}' where id_parent = '{}'".format(coin_transaction_to_parent,
                                                                                       id_p))
            conn.commit()
            conn.close()