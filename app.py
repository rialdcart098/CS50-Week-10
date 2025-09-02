import os

from flask import Flask, session, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from markupsafe import Markup, escape
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_db, close_db, user_data, valid_username, valid_password
from datetime import datetime
from routes.quiz import quiz_bp
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'database.db')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(quiz_bp)


@app.teardown_appcontext
def teardown(exception):
    close_db(exception)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
@login_required #Work on this once you get home
def index():
    return render_template("index.html", page="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        for field in ("username", "password"):
            if not request.form[field]:
                return render_template("login.html", page="login", error=f"Please fill out your {field}.")
        username = request.form["username"]
        password = request.form["password"]
        if not user_data(username):
            return render_template("login.html",
                page="login",
                error=Markup(
                    f'User {escape(username)} does not exist. '
                    f'<a href="{url_for("signup")}" style="color:#ff0000; text-decoration:none;">register here.</a>'
                ))
        userData = user_data(username)
        if not check_password_hash(userData["password"], password):
            return render_template("login.html",
                page="login",
                error=Markup('Wrong username/password. Try again.'))
        session["id"] = userData["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == "POST":

        ERRORS = {
            1: "username is missing",
            2: Markup(f'User {escape(request.form["username"])} already exists. '
                f'<a href="{url_for("login")}">log in here</a>" if this is you.'),
            3: "username too long/short (3 < username < 20)",
            4: "username can't have symbols.",

            5: "Password field must be filled.",
            6: "Password must be at least 8 characters.",
            7: "Password must contain at least 1 letter.",
            8: "Password must contain at least 1 number.",
            9: "Password must contain at least 1 symbol.",
            10: "Password must contain at least 1 capital letter",
            11: "Passwords don't match.",

            12: "Confirm field must be filled.",
            13: "Birth date must be filled.",
            14: "Invalid birth date."
        }
        for field in ("password", "confirm_password", "birth"):
            if not request.form[field]:
                return render_template("signup.html", page="Sign Up", error=f"Missing field: {field}")

        if valid_username(request.form["username"]) is not True:
            return render_template("signup.html",
                page="Sign Up",
                error=ERRORS[valid_username(request.form["username"])])
        
        try:
            birth = datetime.strptime(request.form["birth"], "%Y-%m-%d").date()
        except ValueError:
            return render_template('signup.html',
                page="signup",
                error=Markup(
                    f'Birth date {escape(request.form["birth"])} is not valid. '
                ))
        if valid_password(request.form["password"], request.form["confirm_password"]) is not True:
            return render_template('signup.html',
                page="signup",
                error=ERRORS[valid_password(request.form["password"], request.form["confirm_password"])])

        db = get_db()
        user_id = db.execute("INSERT INTO users (username, password, birth) VALUES (?, ?, ?)",
            (request.form["username"], generate_password_hash(request.form["password"]), birth)
            ).lastrowid
        db.commit()

        session["id"] = user_id
        return redirect("/")

    return render_template("signup.html", page="signup")

if __name__ == "__main__":
    app.run(debug=True)