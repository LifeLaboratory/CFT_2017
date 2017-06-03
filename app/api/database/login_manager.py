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


def login_in(login, password):
    print (login)
    print(password)
    conn, c = connect_db()
    sql = ("SELECT id_parent FROM parents where login = '{}' and password = '{}'".format(login, password))
    c.execute(sql)
    result = c.fetchall()
    print(result)
    if len(result) != 0:
        return {'id': result[0], 'status': 'parent'}
    sql = ("SELECT id_child FROM children where login = '{}' and password = '{}'".format(login, password))
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    if len(result) != 0:
        return {'id': result[0], 'status': 'children'}
    else:
        return 'Error'
