import sqlite3
import uuid

def create_task(id_parent, id_children, description, coin):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    uid_task = str(uuid.uuid4())
    purchases = [(uid_task, id_parent, id_children, description, coin, '0')]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
