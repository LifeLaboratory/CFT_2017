import sqlite3

def _all(id_c):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    s = c.execute("SELECT description FROM tasks WHERE id='{}'".format(id_c)).fetchall()
    con.commit()
    con.close()
    return(s)

def not_executed(id_c):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    s2 = c.execute("SELECT description FROM tasks WHERE id='{}' AND status=0".format(id_c)).fetchall()
    conn.commit()
    conn.close()
    return print(s2)

def executed(id_c):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    p = c.execute("SELECT description FROM tasks WHERE status=2 AND id='{}'".format(id_c)).fetchall()
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

def checkdone(description, id_c):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{0}' WHERE description='{1}' AND id_child='{2}'".format(1, description, id_c)
    c.execute(sql)
    con.commit()
    con.close()
