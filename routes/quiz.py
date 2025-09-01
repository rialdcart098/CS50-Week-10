from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, g, current_app
from flask_session import Session
from markupsafe import Markup, escape
from helpers import login_required
import sqlite3
import os

app = Flask(__name__)

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates/quizzes', url_prefix='/quizzes')

@quiz_bp.route("/", methods=["GET", "POST"])
@login_required
def quiz_home():

    return render_template("quizzes.html", page="Quiz")