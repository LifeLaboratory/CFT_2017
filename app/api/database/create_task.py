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


def create_task(id_children, id_parent, description, coin):
    conn, c = connect_db()
    uid_task = str(uuid.uuid4())
    purchases = [(uid_task, id_children, id_parent, description, coin, 'open')]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


