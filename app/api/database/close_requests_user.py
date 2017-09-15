
import uuid

#for other os
from app.api.database.connect_db import connect_db


def close_requests_user(id_task):
    '''
    Закрытие запроса.
    Изменение статуса на 1
    '''
    conn, c = connect_db()
    sql = "update requests SET status = 1 "\
                  "where id_requests = '{0}'".format(id_task)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()
