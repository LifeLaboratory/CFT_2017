import sqlite3

def _all():
    con = sqlite3.connect("database.db")
    c = con.cursor()
    s = c.execute("SELECT description FROM tasks").fetchall()
    con.commit()
    con.close()
    return(s)

def not_executed():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    s2 = c.execute("SELECT description FROM tasks WHERE status=0").fetchall()
    conn.commit()
    conn.close()
    return(s2)

def executed():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    p = c.execute("SELECT description FROM tasks WHERE status=2").fetchall()
    conn.commit()
    conn.close()
    return(p)

def done(id_task):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{}' WHERE id_task='{}'".format(2, id_task)
    c.execute(sql)
    con.commit()
    con.close()

def checkdone(description):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{}' WHERE description='{}'".format(1, description)
    c.execute(sql)
    con.commit()
    con.close()
