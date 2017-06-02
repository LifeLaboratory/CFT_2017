import sqlite3

id_task = {"id_task": '70131fa3-cae0-4733-a55d-bdc8a748fecf',
           }

def done(id_task):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{}' WHERE id_task='{}'".format(
        2, id_task
    )
    c.execute(sql)
    con.commit()
    con.close()

#done(id_task["id_task"])


def checkdone(id_task):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    sql = "UPDATE tasks SET status='{}' WHERE id_task='{}'".format(
        1, id_task
    )
    c.execute(sql)
    con.commit()
    con.close()

#checkdone(id_task["id_task"])