#from connect_db import connect_db

#for linux
import sys
import os
directory_user_cabinet = os.getcwd()
print (directory_user_cabinet)
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db
def login_in(login, password):
    print (login)
    print(password)
    conn, c = connect_db()
    sql = ("SELECT password, id_parent FROM parents where login = '{}'".format(login))
    c.execute(sql)
    result = c.fetchall()
    conn.close
    if password == result[0][0]:
        return result[0][1]
    else:
        return "NO"