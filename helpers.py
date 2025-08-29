import requests

from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrap