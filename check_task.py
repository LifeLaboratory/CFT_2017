import sqlite3
id_parent = {"id_parent": "118122ba-aac4-4dbc-b1da-37abbfc63bfe",
             }


def check_done(id_parent):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = ("SELECT description, coin FROM tasks where id_parent = '{}' and status = '{}'".format(id_parent, 0))
    c.execute(sql)
    result = c.fetchall()
    return (result)

def check_checkdone(id_parent):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = ("SELECT description, coin FROM tasks where id_parent = '{}' and status = '{}'".format(id_parent, 1))
    c.execute(sql)
    result = c.fetchall()
    return (result)

def check_notdone(id_parent):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = ("SELECT description, coin FROM tasks where id_parent = '{}' and status = '{}'".format(id_parent, 2))
    c.execute(sql)
    result = c.fetchall()
    return (result)
print (check_done(id_parent["id_parent"]))
print (check_checkdone(id_parent["id_parent"]))
print (check_notdone(id_parent["id_parent"]))