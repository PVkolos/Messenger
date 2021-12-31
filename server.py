import time
import sqlite3
from hashlib import sha256

from flask import Flask, request, abort

app = Flask(__name__)


@app.route("/")
def hello():
    return 'Messenger'


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': time.time()
    }


@app.route('/send', methods=['POST'])
def send_m():
    """  отправка сообщений в общий чат  """
    data = request.json
    name = data['name']
    if not isinstance(data, dict):
        return abort(400)
    if 'text' not in data:
        return abort(400)
    text = data['text']
    if not isinstance(text, str):
        return abort(400)
    if len(text) == 0 or len(text) > 1000:
        abort(400)

    con = sqlite3.connect('DB/db1.sqlite')
    cur = con.cursor()
    cur.execute(f"""INSERT INTO messages(name, text, time) VALUES('{name}', '{text}', '{time.time()}')""").fetchall()
    con.commit()
    con.close()

    return {'ok': True}


@app.route('/messages')
def get_m():
    """  получение всех сообщений, время отправки которых больше чем after  """
    try:
        after = float(request.args['after'])
    except Exception:
        abort(400)
    con = sqlite3.connect('DB/db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select * from messages where time > {after}""").fetchall()
    con.close()

    return {'messages': result}


@app.route('/users')
def users():
    """  получение списка всех пользователей мессенджера  """
    con = sqlite3.connect('DB/db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select name, password, id, path from users""").fetchall()
    return {'users': result}


@app.route('/insert_users')
def insert_users():
    """  иземенение данных пользователей мессенджера  """
    data = request.json
    name = data['name']
    path = ''
    name2 = ''
    try:
        path = data['path']
    except Exception:
        name2 = data['name2']
    con = sqlite3.connect('DB/db1.sqlite')
    cur = con.cursor()
    if path:
        result = cur.execute(f"""UPDATE users
                        SET path = '{path}'
                        WHERE name = '{name}'""").fetchall()
    elif name2:
        result = cur.execute(f"""UPDATE users
                        SET name = '{name2}'
                        WHERE name = '{name}'""").fetchall()
    con.commit()
    con.close()
    return {'users': result}


@app.route('/add_user', methods=['POST'])
def add_users():
    """  добавление пользователя в мессенджер (т.е. в БД)  """
    data = request.json
    name = data['name']
    password = data['password']
    path = data['path']
    if not name or not password:
        abort(400)
    con = sqlite3.connect('DB/db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select * from users where name='{name}'""").fetchall()
    if not result:
        password = sha256(password.encode('utf-8')).hexdigest()
        cur.execute(
            f"""INSERT INTO users(name, password, path) VALUES('{name}', '{password}', '{path}')""").fetchall()
        con.commit()
        con.close()
    else:
        abort(500)

    return {'ok': True}


@app.route('/add_chat', methods=['POST'])
def add_chat():
    """  добавить личный чат на сервер (создание теблицы в БД с именем 'username1_username2')  """
    data = request.json
    id_one = data['id_one']
    id_two = data['id_two']
    if not id_one or not id_two:
        abort(400)
    lis = [id_one, id_two]
    con = sqlite3.connect('DB/chats.sqlite')
    cur = con.cursor()
    lis.sort()
    name = f'{lis[0]}_{lis[1]}'
    print(name)
    try:
        cur.execute(f"""CREATE TABLE '{name}' (
                                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                    otpr    STRING,
                                    messege STRING,
                                    time    STRING);""").fetchall()
        con.commit()
        con.close()
        print('okkk')
        return {'ok': True}
    except Exception:
        abort(400)


@app.route('/send_ch', methods=['POST'])
def send_messege():
    """   добавление личного сообщения между двумя пользователями. otpr - отправитель сообщения  """
    data = request.json
    name = data['name']
    if not isinstance(data, dict):
        return abort(400)
    if 'messege' not in data or 'otpr' not in data:
        return abort(400)
    messege = data['messege']
    otpr = data['otpr']
    if not isinstance(messege, str) or not isinstance(otpr, str):
        return abort(400)
    if len(messege) == 0 or len(messege) > 1000:
        abort(400)

    con = sqlite3.connect('DB/chats.sqlite')
    cur = con.cursor()
    cur.execute(
        f"""INSERT INTO '{name}'(otpr, messege, time) VALUES('{otpr}', '{messege}', '{time.time()}')""").fetchall()
    con.commit()
    con.close()

    return {'ok': True}


@app.route('/get_messages', methods=['GET', 'POST'])
def get_message():
    """  получение всех сообщений личного чата, время отправки которых больше чем after  """
    try:
        data = request.json
        name = data['name']
        after = float(request.args['after'])
    except Exception:
        abort(400)
    try:
        con = sqlite3.connect('DB/chats.sqlite')
        cur = con.cursor()
        res = cur.execute(
            f"""select otpr, messege, time from '{name}' where time > {after}""").fetchall()
        con.close()
    except Exception as e:
        print(e)
        return

    return {'messages': res[:50]}


app.run()
