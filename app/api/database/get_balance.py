from app.api.database.connect_db import connect_db
from app.api.money.qiwi import QIWI

def balance_child(id):
    '''Полуение баланса ребенка из базы данных'''
    conn, c = connect_db()
    c.execute("SELECT number_open  FROM children WHERE id_child='{}'".format(id))
    result = c.fetchall()
    return [result[0][0]]

#balance_child("Sveta1")


def balance_parent(id):

    '''Полуение баланса родителя из базы данных'''
    conn, c = connect_db()
    c.execute("SELECT balance_parent FROM parents where id_parent = '{}'".format(id))
    result = c.fetchall()
    for i in result[0]:
        result = i

    return result

