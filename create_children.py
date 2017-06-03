from connect_db import connect_db
import uuid

def create_child(id_parent, login, password, name, surname, patronymic, sex,
                 number_close, number_open, number_needs):
    conn, c = connect_db()
    uid_child = str(uuid.uuid4())
    purchases = [(uid_child, id_parent, login, password, name, surname, patronymic, sex,
                 number_close, number_open, number_needs)]
    c.executemany('INSERT INTO children VALUES (?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()