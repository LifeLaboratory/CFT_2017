import uuid
#for other os
from app.api.database.connect_db import connect_db


def create_child(id_parent, login, password, name, surname, patronymic, sex,
                 number_close):
    '''
    Создание записи в таблице детей в базе данных.
    '''
    conn, c = connect_db()
    uid_child = str(uuid.uuid4())
    purchases = [(uid_child, id_parent, login, password, name, surname, patronymic, sex, 0, 0, 0,
                 number_close, 0, 0)]
    c.executemany('INSERT INTO children VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()