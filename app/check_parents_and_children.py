import sqlite3



def check_login(login):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql=("SELECT * FROM parents where login = '{}'".format(login))
    c.execute(sql)
    result = c.fetchall()
    if len(result) != 0:
        return "Login_parent is busy"
    else:
            return (0)
