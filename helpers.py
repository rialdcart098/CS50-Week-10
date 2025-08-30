import string
from flask import session, redirect, g, current_app
from functools import wraps
import sqlite3



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('user_id'):
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

def valid_username(username):
    if not username:
        return False
    if not user_data(username):
        return False
    if len(username) < 3 or len(username) > 20:
        return False
    for char in username:
        if not char.isalpha() or not char.isnum():
            return False
    return True

def valid_password(password):
    if not password:
        return False
    character = False
    number = False
    Symbol = False
    Capital = False
    if len(password) < 8:
        return False
    for char in password:
        if char.isalpha():
            character = True
        elif char.isdigit():
            number = True
        elif not char.isalnum():
            Symbol = False
        elif char.isupper() == char:
            character = True
    if all([character, number, Symbol, Capital]):
        return True
    return False

def valid_date(date):
    if not date:
        return False
