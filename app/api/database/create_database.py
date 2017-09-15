#from connect_db import connect_db


from app.api.database.connect_db import connect_db

'''
Функции для создания чистой базы данных
'''

def create_table_parents():
    conn, c = connect_db()
    c.execute('''create table parents (id_parent varchar(255), id_child varchar(255), login varchar(255),
        password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255),
        sex varchar(255), balance_needs int, balance_close int, balance_open int,
        balance_parent int, tel_number int)''')

    conn.commit()
    conn.close()
#


def create_table_children():
    conn, c = connect_db()
    c.execute('''create table children (id_child varchar(255), id_parent varchar(255), login varchar(255),
        password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255),
        sex varchar(255), balance_needs int, balance_close int, balance_open int, 
        number_close int, number_open int, number_needs int)''')
    conn.commit()
    conn.close()
#


def create_table_tasks():
    conn, c = connect_db()
    c.execute('''create table tasks (id_task varchar(255), id_parent varchar(255), id_child int,
        description varchar(255), coin int, status int)''')
    conn.commit()
    conn.close()
#


def create_table_regex():
    conn, c = connect_db()
    c.execute('''create table regex (id_regex varchar(255), id_child varchar(255),
        description varchar(255))''')
    conn.commit()
    conn.close()
#


def create_table_requests():
    conn, c = connect_db()
    c.execute('''create table requests (id_requests varchar(255), id_child varchar(255), id_parent varchar(255),
        description varchar(255), coin int, status int)''')
    conn.commit()
    conn.close()



create_table_requests()
create_table_parents()
create_table_regex()
create_table_children()
create_table_tasks()
