import uuid

#for other os
from app.api.database.connect_db import connect_db



def create_regex(id_children, description):
    '''Создание записи в таблице нужд'''
    conn, c = connect_db()
    uid_regex = str(uuid.uuid4())
    purchases = [(uid_regex, id_children, description)]
    c.executemany('INSERT INTO regex VALUES (?,?,?)', purchases)
    conn.commit()
    conn.close()


