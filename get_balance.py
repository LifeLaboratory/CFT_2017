import sqlite3

def balance_child(id_child):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT balance_needs, balance_open, balance_close FROM children WHERE id_child='{}'".format(id_child))
    result = c.fetchall()
    needs = result[0][0]
    _open = result[0][1]
    close = result[0][2]
    return ("Needs:{0}, Close{1}, Open:{2}".format(needs, close, _open))

def balance_parent(id_parent):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT balance_needs FROM parents where id_parent='{}'".format(id_parent))
    result = c.fetchall()
    for i in result[0]:
        result = i
    return(result)
