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


def close_task_user(id_task, id_user, status):
    conn, c = connect_db()
    sql = "update tasks SET status = '{0}' "\
                  "where id_task = '{1}' and "\
                  "(id_child = '{2}' or id_parent = '{3}')".format(status, id_task, id_user, id_user)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()


