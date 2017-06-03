#from connect_db import connect_db
"""
import sys
import os
directory_user_cabinet = os.getcwd()
print (directory_user_cabinet)
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db
"""

from app.api.database.connect_db import connect_db


def create_table_parents():
    conn, c = connect_db()
    c.execute('''create table parents (id_parent varchar(255), id_child varchar(255), login varchar(255),
        password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255),
        sex varchar(255), number_parents int, balance_needs int, balance_close int, balance_open int, balance_parent int, tel_number int )''')

    conn.commit()
    conn.close()
create_table_parents()


def create_table_children():
    conn, c = connect_db()
    c.execute('''create table children (id_child varchar(255), id_parent varchar(255), login varchar(255),
        password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255),
        sex varchar(255), number_close int, number_open int, number_needs int)''')
    conn.commit()
    conn.close()
create_table_children()


def create_table_tasks():
    conn, c = connect_db()
    c.execute('''create table tasks (id_task varchar(255), id_parent varchar(255), id_child int,
        description varchar(255), coin int, status int)''')
    conn.commit()
    conn.close()
create_table_tasks()
