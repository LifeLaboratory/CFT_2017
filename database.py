import sqlite3
import uuid
from check_parents_and_children import check_login

def create_table_parents():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table parents (id_parent varchar(255), id_child varchar(255), login varchar(255), 
    password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255), 
    sex varchar(255), number_parents int, number_close int, number_open int, number_needs int, 
    balance_needs int, balance_close int, balance_open int )''')
    conn.commit()
    conn.close()
#create_table_parents()


def create_table_children():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table children (id_child varchar(255), id_parent varchar(255), login varchar(255), 
    password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255), 
    sex varchar(255), number_close int, number_open int, number_needs int, balance_needs int, 
    balance_open )''')
    conn.commit()
    conn.close()
#reate_table_children()

def create_table_tasks():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table tasks (id_task varchar(255), id_parent varchar(255), id_child int, 
    description varchar(255), coin int, status int)''')
    conn.commit()
    conn.close()
#create_table_tasks()

def create_parent():
    data = {"login": "Sveta1",
            "password": "Sveta2",
            "name": "Sveta",
            "surname": "Ivanova",
            "patronymic": "Ivanovna",
            "sex": "woman",
            "number_parents": 8888777799994441,
            "number_close": 8888777799994442,
            "number_open": 8888777799994443,
            "number_needs": 8888777799994444,
            "tel_number": 88005553535,
            "login_child": "Max1",
            "password_child": "Max2",
            "name_child": "Max",
            "surname_child": "Petrov",
            "patronymic_child": "Egorovich",
            "sex_child": "man",
            }
    answer_check=check_login(data)
    if answer_check!=0:
        print (answer_check["Answer"])
    else:
        conn=sqlite3.connect('database.db')
        c = conn.cursor()
        uid_parent = str(uuid.uuid4())
        uid_child = str(uuid.uuid4())
        purchases = [(uid_parent, uid_child, data["login"], data["password"], data["name"],
                      data["surname"], data["patronymic"], data["sex"], data["number_parents"],
                      data["number_close"], data["number_open"], data["number_needs"])]
        #print (purchases)
        c.executemany('INSERT INTO parents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,0,0,0)', purchases)
        purchases = [(uid_child, uid_parent, data["login_child"], data["password_child"],
                      data["name_child"], data["surname_child"], data[("patronymic_child")],
                      data["sex_child"], data["number_close"], data["number_open"],
                      data["number_needs"])]
        c.executemany('INSERT INTO children VALUES (?,?,?,?,?,?,?,?,?,?,?,0,0)', purchases)
        conn.commit()
        conn.close()
#create_parent()

def create_task():
    data = {"id_parent": "123c81b7-b9aa-44d3-bb36-dd7f49d248b0",
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
    purchases = [(uid_task, data["id_parent"], idchild, data["description"],
                  data["coin"], status)]
    c.executemany('INSERT INTO tasks VALUES (?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
#create_task()

def get_table(table):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    result = cur.fetchall()
    con.close
    return result

#print(get_table('parents'))
#print(get_table('children'))
#print(get_table('tasks'))