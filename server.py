import time
import sqlite3
from hashlib import sha256

from flask import Flask, request, abort

app = Flask(__name__)


@app.route("/")
def hello():
    return 'Привет'


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': time.time()
    }


@app.route('/send', methods=['POST'])
def send_m():
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

    con = sqlite3.connect('db1.sqlite')
    cur = con.cursor()
    cur.execute(f"""INSERT INTO messages(name, text, time) VALUES('{name}', '{text}', '{time.time()}')""").fetchall()
    con.commit()
    con.close()

    return {'ok': True}


@app.route('/messages')
def get_m():
    try:
        after = float(request.args['after'])
    except Exception:
        abort(400)
    con = sqlite3.connect('db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select * from messages where time > {after}""").fetchall()
    con.close()

    return {'messages': result[:50]}


@app.route('/users')
def users():
    con = sqlite3.connect('db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select name, password from users""").fetchall()
    return {'users': result}


@app.route('/add_user', methods=['POST'])
def add_users():
    data = request.json
    name = data['name']
    password = data['password']
    if not name or not password:
        abort(400)
    con = sqlite3.connect('db1.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""select * from users where name='{name}'""").fetchall()
    if not result:
        password = sha256(password.encode('utf-8')).hexdigest()
        cur.execute(
            f"""INSERT INTO users(name, password) VALUES('{name}', '{password}')""").fetchall()
        con.commit()
        con.close()
    else:
        abort(500)

    return {'ok': True}


app.run()