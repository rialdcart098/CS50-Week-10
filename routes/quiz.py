from flask import Flask, Blueprint, render_template, session
from helpers import login_required

app = Flask(__name__)

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates/quizzes', url_prefix='/quizzes')

@quiz_bp.route("/", methods=["GET", "POST"])
@login_required
def quiz_home():
    return render_template("quizzes.html", page="Quiz Menu")

@quiz_bp.route("/<quizname>")
@login_required
def quiz_page(quizname):
    return render_template("quiz-page.html", page="Quiz", exam=quizname)