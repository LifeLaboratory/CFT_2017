import sqlite3

login_child = {"login_child": 'Max1',
               }
def balance_child(login):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = ("SELECT balance_needs, balance_open FROM children where login = '{}'".format(login))
    c.execute(sql)
    result = c.fetchall()
    return (result)

login_parent = {"login_child": 'Sveta1',
                }
def balance_parent(login):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = ("SELECT balance_needs, balance_close, balance_open FROM parents where login = '{}'".format(login))
    c.execute(sql)
    result = c.fetchall()
    return (result)

print (balance_child(login_child["login_child"]))
print (balance_parent(login_parent["login_child"]))