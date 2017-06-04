import sqlite3

def check_login(data):

    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT * FROM parents where login = '{}'".format(data["login"]))
    result = c.fetchall()
    if len(result) != 0:
        return {"Answer": "Login_parent is busy"}
    else:
        sql = ("SELECT * FROM children where login = '{}'".format(data["login_child"]))
        c.execute(sql)
        result = c.fetchall()
        con.close
        if len(result) != 0:
            return {"Answer": "Login_child is busy"}
        else:
            return (0)
