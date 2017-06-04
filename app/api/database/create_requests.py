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


def create_requests(id_children, description, coin):
    conn, c = connect_db()
    uid_regex = str(uuid.uuid4())
    sql = "SELECT id_parent FROM children where id_child = '{}'".format(id_children)
    c.execute(sql)
    id_parent = c.fetchall()[0][0]
    purchases = [(uid_regex, id_children, id_parent, description, coin)]
    c.executemany('INSERT INTO requests VALUES (?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()


