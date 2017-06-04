import sqlite3

def get_table(table):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    result = cur.fetchall()
    con.close
    return (result)

print(get_table('parents'))
print(get_table('children'))
print(get_table('tasks'))
