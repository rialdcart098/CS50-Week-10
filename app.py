from flask import url_for, Flask, session, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = sqlite3.connect("database.db")
cur = db.cursor()

@app.route("/")
@login_required
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
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cur.fetchone()[0] != 1:
            return render_template("login.html",
                page="login",
                error=Markup(
                    f'User {username} does not exist. <a href="{url_for("register")}" style="color:#ff0000; text-decoration:none;">register here.</a>'
                ))



        return redirect("/")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == "POST":
        for field in ("username", "password"):
            if not request.form[field]:
                return render_template("login.html", page="login", error=f"Missing field: {field}")


if __name__ == "__main__":
    app.run(debug=True)