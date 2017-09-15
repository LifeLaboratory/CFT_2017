import sqlite3


def connect_db():
    '''
    Подключение к базе данных лежащей в корне
    '''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c