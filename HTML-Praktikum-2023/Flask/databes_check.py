import sqlite3
from datetime import datetime
import hashlib
import threading


def hash_value(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def checkUser(user, password):
    conn = sqlite3.connect("users.db")
    curser = conn.cursor()
    try:
        curser.execute("SELECT password FROM users WHERE username=?", (user,))
        database_password = curser.fetchall()[0][0]
    except:
        return False
    print(database_password)
    password = str(password)
    if database_password == hash_value(password):
        return True
    return False


def exist(username):
    conn = sqlite3.connect("users.db")
    curser = conn.cursor()
    try:
        curser.execute("Select rechte FROM users WHERE username=?", (username,))
        print("Exist: ",curser.fetchall()[0][0])
        print("User not exist")
        return True
    except:
        print("True")
        return False


def add_user(username, password, erstellt_von, rechte):
    if not exist(username):
        conn = sqlite3.connect("users.db")
        curser = conn.cursor()
        werte = [(username, hash_value(password), datetime.today().strftime('%Y-%m-%d %H:%M'), erstellt_von, rechte)]
        curser.executemany("INSERT INTO users VALUES(?,?,?,?,?)", werte)
        conn.commit()


def delete_user(username):
    conn = sqlite3.connect("users.db")
    curser = conn.cursor()
    curser.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


def change_value(username, old_value_class, new_value):
    if old_value_class == "change_password":
        conn = sqlite3.connect("users.db")
        curser = conn.cursor()
        curser.execute("UPDATE users set password = ? WHERE username=?", (hash_value(new_value), username))
        conn.commit()


def return_values(value=None, all=False, user=None):
    if all:
        conn = sqlite3.connect("users.db")
        curser = conn.cursor()
        curser.execute("SELECT * FROM users")
        zeilen = curser.fetchall()

        # for i in zeilen:
        #     print(i)
        return zeilen
    elif value == "rang":
        conn = sqlite3.connect("users.db")
        curser = conn.cursor()
        curser.execute("SELECT rechte FROM users WHERE username = ?", (user,))
        zeilen = curser.fetchall()
        # for i in zeilen:
        #     print(i)
        return zeilen[0][0]


if __name__ == '__main__':
    # conn = sqlite3.connect("users.db")
    # cursor = conn.cursor()
    # cursor.execute("create table users(username text, password text, erstelldatum text, erstellt von text, rechte integer)")
    # add_user("Tobias", "1234", "SYSTEM", 0)
    print(return_values(value="rang", user="Tobias"))
