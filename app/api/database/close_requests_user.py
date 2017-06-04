
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


def close_requests_user(id_task):
    conn, c = connect_db()
    sql = "update requests SET status = 1 "\
                  "where id_requests = '{0}'".format(id_task)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()
