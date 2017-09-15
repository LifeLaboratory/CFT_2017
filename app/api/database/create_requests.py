import uuid

#for other os
from app.api.database.connect_db import connect_db


def create_requests(id_children, description, coin):
    '''Создание записи в таблице запросов'''
    conn, c = connect_db()
    uid_regex = str(uuid.uuid4())
    sql = "SELECT id_parent FROM children where id_child = '{}'".format(id_children)
    c.execute(sql)
    id_parent = c.fetchall()[0][0]
    purchases = [(uid_regex, id_children, id_parent, description, coin, 0)]
    c.executemany('INSERT INTO requests VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


