from app.api.database.connect_db import connect_db


def balance_child(id):
    conn, c = connect_db()
    c.execute("SELECT balance_needs, balance_open, balance_close FROM children WHERE id_child='{}'".format(id))
    result = c.fetchall()
    print(result)
    return [result[0][0], result[0][1], result[0][2]]

#balance_child("Sveta1")


def balance_parent(id):
    conn, c = connect_db()
    c.execute("SELECT balance_needs FROM parents where id_parent = '{}'".format(id))
    result = c.fetchall()
    for i in result[0]:
        result = i
    return result

