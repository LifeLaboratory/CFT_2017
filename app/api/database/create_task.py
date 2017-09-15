import uuid

#for other os
from app.api.database.connect_db import connect_db



def create_task(id_parent, id_children, description, coin):
    '''
    Создание записи в таблице задач.
    '''
    conn, c = connect_db()
    uid_task = str(uuid.uuid4())
    purchases = [(uid_task, id_children, id_parent, description, coin, '0')]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


