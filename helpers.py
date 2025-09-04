from flask import session, redirect, g, current_app
from functools import wraps
import sqlite3
import json
import os


# Fixed
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("id"):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrap

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def user_data(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone()

def valid_username(username=None):
    if not username:
        return 1
    if user_data(username):
        return 2
    if len(username) < 3 or len(username) > 20:
        return 3
    for char in username:
        if not char.isalnum():
            return 4
    return True

def valid_password(password, confirm):
    if not password:
        return 5
    conditions = {7: False, 8: False, 9: False, 10: False}
    if len(password) < 8:
        return 6
    for char in password:
        if char.isalpha():
            if char.isupper():
                conditions[10] = True
            conditions[7] = True
        elif char.isdigit():
            conditions[8] = True
        elif not char.isalnum():
            conditions[9] = True
    for index, condition in conditions.items():
        if not condition:
            return index

    if not confirm:
        return 11
    elif password != confirm:
        return 12
    return True

def load_json(filename):
    file = f'quizzes/{filename}.json'
    if not os.path.exists(file):
        raise FileNotFoundError
    with open(file, 'r') as f:
        return json.load(f)