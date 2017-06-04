import sqlite3
import uuid

def _task(id_parent, description, coin):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id_child FROM parents where id_parent = '{}'".format(id_parent))
    conn.commit()
    idchild = c.fetchall()
    idchild = idchild[0][0]
    uid_task = str(uuid.uuid4())
    status = 0
    purchases = [(uid_task, id_parent, idchild, description, coin, status)]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
