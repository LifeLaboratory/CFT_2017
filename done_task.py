import sqlite3

def _all(id_p):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    s = c.execute("SELECT description FROM tasks WHERE id_parent='{}'".format(id_p)).fetchall()
    con.commit()
    con.close()
    return (s)

def not_executed(id_p):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    s2 = c.execute("SELECT description FROM tasks WHERE id_parent='{}' AND status=0".format(id_p)).fetchall()
    conn.commit()
    conn.close()
    return (s2)

def executed(id_p):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    p = c.execute("SELECT description FROM tasks WHERE status=2 AND id_parent='{}'".format(id_p)).fetchall()
    conn.commit()
    conn.close()
    return(p)

def done(id_task):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{0}' WHERE id_task='{1}'".format(2, id_task)
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
