import uuid

#for other os
from app.api.database.connect_db import connect_db



def close_task_user(id_task, id_user, status):
    '''
    Закрытие задач.
    Установление статуса 1, если было 0.
    Установление статуса 2, если было 1.
    '''
    conn, c = connect_db()
    sql = "update tasks SET status = '{0}' "\
                  "where id_task = '{1}' and "\
                  "(id_child = '{2}' or id_parent = '{3}')".format(status, id_task, id_user, id_user)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()


