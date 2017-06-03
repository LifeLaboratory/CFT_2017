import uuid
from connect_db import connect_db


def create_task(id_parent, description, coin):
    conn, c = connect_db()
    uid_task = str(uuid.uuid4())
    '''
    c.execute('''create table tasks (id_task varchar(255), id_parent varchar(255), id_child int,
            description varchar(255), coin int, status int)''')
                          '''
        conn.commit()
    conn.close()