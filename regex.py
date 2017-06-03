import sqlite3

def regex(id_child, description):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    c.execute("SELECT * FROM regex WHERE id_child='{0}' AND description ='{1}'".format(id_child, description))
    result = c.fetchall()
    conn.close()
    if len(result) != 0:
        return(True)
    else:
        return(False)
