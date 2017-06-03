import uuid
#for other os
from app.api.database.connect_db import connect_db

#for linux
"""
import sys
import os
#directory_user_cabinet = os.getcwd()
directory_user_cabinet="/home/raldenprog/CFT/the_best_service/hackaton_cft/app/api/database"
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db
"""


def create_child(id_parent, login, password, name, surname, patronymic, sex,
                 number_close, number_open, number_needs):
    conn, c = connect_db()
    uid_child = str(uuid.uuid4())
    purchases = [(uid_child, id_parent, login, password, name, surname, patronymic, sex,
                 number_close, number_open, number_needs)]
    c.executemany('INSERT INTO children VALUES (?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()