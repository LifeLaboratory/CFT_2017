import sqlite3

def create_table():
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''create table parents (id_parent INTEGER PRIMARY KEY, id_child int, login varchar(255), password varchar(255), name varchar(255), surname varchar(255), patronymic varchar(255), sex varchar(255), number_parents int, number_close int, number_open int, number_needs int )''')
    conn.commit()
    conn.close()
#create_table()

def create_parent():
    data = {"id_child": 1,
            "login": "Maria1",
            "password": "Maria2",
            "name": "Maria",
            "surname": "Petrova",
            "patronymic": "Egorovna",
            "sex": "woman",
            "number_parents": 8888777799994441,
            "number_close": 8888777799994442,
            "number_open": 8888777799994443,
            "number_needs": 8888777799994444,
            }
    conn=sqlite3.connect('database.db')
    c = conn.cursor()
    purchases = [(data["id_child"], data["login"], data["password"], data["name"], data["surname"], data["patronymic"], data["sex"], data["number_parents"], data["number_close"], data["number_open"], data["number_needs"])]
    print (purchases)
    c.executemany('INSERT INTO parents VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)', purchases)
    conn.commit()
    conn.close()
create_parent()

def get_table(table):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    result = cur.fetchall()
    con.close
    return result

print (get_table('parents'))
