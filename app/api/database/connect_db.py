import sqlite3


def connect_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c