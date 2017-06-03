import sqlite3

def balance_child(login):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT balance_needs, balance_open, balance_close FROM parents WHERE login='{}'".format(login))
    result = c.fetchall()
    needs = result[0][0]
    _open = result[0][1]
    close = result[0][2]
    return ("Needs:{0}, Close{1}, Open:{2}".format(needs, close, _open))

#balance_child("Sveta1")

def balance_parent(login):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT balance_parent FROM parents where login = '{}'".format(login))
    result = c.fetchall()
    for i in result[0]:
        result = i
    return(result)

#balance_parent("Sveta1")
