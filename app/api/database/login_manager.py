from app.api.database.connect_db import connect_db


def login_in(login, password):
    '''
    Функция входа
    '''
    print (login)
    print(password)
    conn, c = connect_db()
    sql = ("SELECT id_parent FROM parents where login = '{}' and password = '{}'".format(login, password))
    c.execute(sql)
    print(sql)
    result = c.fetchall()
    print(result)
    if len(result) != 0:
        return {'id': result[0], 'status': 'parent'}
    sql = ("SELECT id_child FROM children where login = '{}' and password = '{}'".format(login, password))
    c.execute(sql)
    print(sql)
    result = c.fetchall()
    conn.close()
    if len(result) != 0:
        return {'id': result[0], 'status': 'children'}
    else:
        return 'Error'
