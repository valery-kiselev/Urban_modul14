import sqlite3


connection = sqlite3.connect('prod_basa.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('prod_basa.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    prod = cursor.fetchall()
    connection.commit()
    connection.close()
    return prod

def add_user(username, email, age, balance=1000):
    connection = sqlite3.connect('prod_basa.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users VALUES(NULL, ?, ?, ?, ?)', (username, email, age, balance))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('prod_basa.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.commit()
    connection.close()
    if user:
        return True
    else:
        return False
    return user

initiate_db()

