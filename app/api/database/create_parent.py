import uuid

#for other os
#from app.api.database.connect_db import connect_db

#for linux
import sys
import os
directory_user_cabinet = os.getcwd()
print (directory_user_cabinet)
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db


def create_parent(login, password, name, surname, patronymic, sex, number_parents, 
                  balance_needs, balance_close, balance_open, balance_parent, tel_number):
    conn, c = connect_db()
    uid_parent = str(uuid.uuid4())
    uid_child = "nothing"
    purchases = [(uid_parent, uid_child, login, password, name, surname, patronymic,
                sex, number_parents, balance_needs, balance_close, balance_open,
                balance_parent, tel_number)]
    #print (purchases)
    c.executemany('INSERT INTO parents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


