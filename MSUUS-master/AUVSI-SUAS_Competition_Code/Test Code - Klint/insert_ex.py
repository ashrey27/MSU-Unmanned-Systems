import sqlite3

#conn = sqlite3.connect(path)
#c = conn.cursor()

def create_necessary():
    conn = sqlite3.connect('test/tut.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS test(name TEXT, visited TEXT, value INTEGER)')

def insert(name, visited, value, conn, c):
    c.execute('INSERT INTO test(name, visited, value) VALUES (?,?,?)',
              (name, visited, value))
    conn.commit()