import sqlite3


def connect_db():
    conn = sqlite3.connect('C:\python\hackaton_cft\database.db')
    c = conn.cursor()
    return conn, c