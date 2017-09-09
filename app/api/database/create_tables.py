import uuid
#for other os
from connect_db import connect_db

#for linux
"""
import sys
import os
#directory_user_cabinet = os.getcwd()
directory_user_cabinet="/home/raldenprog/CFT/the_best_service/hackaton_cft/app/api/database"
sys.path.insert(0, directory_user_cabinet)
from connect_db import connect_db
"""
token = '501cc08fac3bd4d08b54d77f4b6ff746'


def create_qiwi_api():
    conn, c = connect_db()
    uid_child = str(uuid.uuid4())
    table = """
    create table tokenQIWI(
        idToken integer not null primary key,
        token varchar(32),
        parent integer not null,
        status integer
    )
    """
    c.executemany(table)
    conn.commit()
    conn.close()

