import sqlite3
import uuid

def create_table_parents():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table parents (id_parent int, id_child int, login varchar(255), password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255), sex varchar(255), number_parents int, number_close int, number_open int, number_needs int )''')
    conn.commit()
    conn.close()
#create_table_parents()


def create_table_children():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table children (id_child int, id_parent int, login varchar(255), password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255), sex varchar(255), number_close int, number_open int, number_needs int )''')
    conn.commit()
    conn.close()
#create_table_children()

def create_table_tasks():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table tasks (id_task int, id_parent int, id_child int, description varchar(255), coin int, status int)''')
    conn.commit()
    conn.close()
#create_table_tasks()

def create_parent():
    data = {"login": "Maria1",
            "password": "Maria2",
            "name": "Maria",
            "surname": "Petrova",
            "patronymic": "Egorovna",
            "sex": "woman",
            "number_parents": 8888777799994441,
            "number_close": 8888777799994442,
            "number_open": 8888777799994443,
            "number_needs": 8888777799994444,
            "tel_number": 88005553535,
            "login_child": "Andrew1",
            "password_child": "Andrew2",
            "name_child": "Maria",
            "surname_child": "Petrova",
            "patronymic_child": "Egorovna",
            "sex_child": "woman",
            }
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    uid_parent = str(uuid.uuid4())
    uid_child = str(uuid.uuid4())
    purchases = [(uid_parent, uid_child, data["login"], data["password"], data["name"], data["surname"], data["patronymic"], data["sex"], data["number_parents"], data["number_close"], data["number_open"], data["number_needs"])]
    #print (purchases)
    c.executemany('INSERT INTO parents VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', purchases)
    purchases = [(uid_child, uid_parent, data["login_child"], data["password_child"], data["name_child"], data["surname_child"], data[("patronymic_child")], data["sex_child"], data["number_close"], data["number_open"], data["number_needs"])]
    c.executemany('INSERT INTO children VALUES (?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
#create_parent()

def create_task():
    data = {"id_parent": "df37b8fa-0ddb-4f72-a3c4-9ac13337ee3a",
            "description": 'Kill heretics',
            "coin": 100500,
            }
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id_child FROM parents where id_parent = '{}'".format(
        data["id_parent"]
    ))
    conn.commit()
    idchild = c.fetchall()[0][0]
    uid_task = str(uuid.uuid4())
    status = 0
    purchases = [(uid_task, data["id_parent"], idchild, data["description"], data["coin"], status)]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
create_task()

def get_table(table):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    result = cur.fetchall()
    con.close
    return result

print(get_table('parents'))
print(get_table('children'))
print(get_table('tasks'))