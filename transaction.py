import sqlite3

class transaction():

    #нужды
    def to_needs(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT number_parents FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("UPDATE parents SET number_parents='{}'".format(coin_transaction_from_parents))
        #Получаем сумму на счету ребенка
        coin_children_all = c.execute("SELECT number_needs FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_all[0]:
            coin_children_all = i
        #зачисляем ему на счет сумму
        coin_transaction_to_children = int(coin_children_all) + int(coin)
        c.execute("UPDATE children SET number_needs='{}'".format(coin_transaction_to_children))
        conn.commit()
        conn.close()

    #в закрытый
    def to_close(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем общую сумму из базы родителей
        coin_parents_all = c.execute("SELECT number_parents FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("UPDATE parents SET number_parents='{}'".format(coin_transaction_from_parents))
        #Получаем сумму на закрытом счету ребенка
        coin_children_close = c.execute("SELECT number_close FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_close[0]:
            coin_children_close = i
        #зачисляем ему на закрытый счет сумму
        coin_transaction_to_children = int(coin_children_close) + int(coin)
        c.execute("UPDATE children SET number_close='{}'".format(coin_transaction_to_children))
        conn.commit()
        conn.close()

    #закрытый-открытый
    def in_close_to_open(coin, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #получаем сумму из закрытого счета ребенка
        coin_children_close = c.execute("SELECT number_close FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_close[0]:
            coin_children_close = i
        #получаем сумму из открытого счета
        coin_children_open = c.execute("SELECT number_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_open[0]:
            coin_children_open = i
        #Списываем сумму с закрытого
        coin_transaction_from_close = int(coin_children_close) - int(coin)
        c.execute("UPDATE children SET number_close='{}'".format(coin_transaction_from_close))
        #Записываем на открытый счет
        coin_transaction_to_open = int(coin_children_open) + int(coin)
        c.execute("UPDATE children SET number_open='{}'".format(coin_transaction_to_open))
        conn.commit()
        conn.close()

    def bonus(coin, id_p, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_parents_all = c.execute("SELECT number_parents FROM parents WHERE id_parent='{}'".format(id_p)).fetchall()
        for i in coin_parents_all[0]:
            coin_parents_all = i
        #coin - значение, которое будет списано и переведено ребенку. Списываем сумму со счета родителей
        coin_transaction_from_parents = int(coin_parents_all) - int(coin)
        c.execute("UPDATE parents SET number_parents='{}'".format(coin_transaction_from_parents))
        #получаем сумму из открытого счета ребенка
        coin_children_open = c.execute("SELECT number_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_open[0]:
            coin_children_open = i
        #Записываем на открытый счет
        coin_transaction_to_open = int(coin_children_open) + int(coin)
        c.execute("UPDATE children SET number_open='{}'".format(coin_transaction_to_open))
        conn.commit()
        conn.close()

    def mulctl(coin, id_c):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        coin_children_open = c.execute("SELECT number_open FROM children WHERE id_child='{}'".format(id_c)).fetchall()
        for i in coin_children_open[0]:
            coin_children_open = i
        coin_transaction_to_open = int(coin_children_open) - int(coin)
        c.execute("UPDATE children SET number_open='{}'".format(coin_transaction_to_open))
        conn.commit()
        conn.close()

transaction.to_needs(10, 'cbe619ef-c870-4925-96ba-3ecabb5e1b42', 'c599719a-fa31-493a-a4e3-8115fd229c07')
transaction.in_close_to_open(20, 'c599719a-fa31-493a-a4e3-8115fd229c07')
transaction.to_close(10, 'cbe619ef-c870-4925-96ba-3ecabb5e1b42', 'c599719a-fa31-493a-a4e3-8115fd229c07')
transaction.bonus(10, 'cbe619ef-c870-4925-96ba-3ecabb5e1b42', 'c599719a-fa31-493a-a4e3-8115fd229c07')
transaction.mulctl(10, 'c599719a-fa31-493a-a4e3-8115fd229c07')
