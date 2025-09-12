from flask import Flask, Blueprint, request, jsonify, session, render_template
from helpers import get_db, unit_fetch
import sqlite3
import math

app = Flask(__name__)

results_bp = Blueprint('results', __name__, template_folder='../templates/results', url_prefix='/results')


@results_bp.route('/', methods=['POST'])
def results():
    results = request.get_json()
    totalQuestion = results['totalQuestions']
    correctAnswers = results['questionsCorrect']
    score = round((correctAnswers / totalQuestion) * 100)
    db = get_db()
    subject = db.execute(
        "SELECT subject FROM subjects WHERE id = ?", (results['subject'],)
    )
    cur = db.execute("INSERT INTO tests (user_id, test, score, subject_id, subject_name, question_amount) VALUES (?, ?, ?, ?, ?, ?)", (
        session['id'],
        results['exam'],
        score,
        results['subject'],
        subject.fetchone()['subject'],
        totalQuestion

    ))
    unitsDone = results['units']
    unitsCorrect = results['unitsCorrect']
    for unit, amount in enumerate(unitsDone):
        if not amount or not unit:
            continue
        elif unit_fetch(unit) <= 0:
            db.execute("INSERT INTO user_progress (questionsDone, questionsCorrect, unit_id, user_id, subject_id) VALUES (?, ?, ?, ?, ?)", (
                amount if amount else 0,
                unitsCorrect[unit] if unit < len(unitsCorrect) and unitsCorrect[unit] else 0,
                unit,
                session['id'],
                results['subject']
            ))
        else:
            db.execute(
                "UPDATE user_progress SET questionsDone = questionsDone + ?,"
                " questionsCorrect = questionsCorrect + ? WHERE unit_id = ? AND user_id = ?",
            (amount if amount else 0,
             unitsCorrect[unit] if unit < len(unitsCorrect) and unitsCorrect[unit] else 0,
             unit,
             session['id']
             ))
    db.commit()
    testID = cur.lastrowid
    return jsonify({"status": "ok", "testID": testID})


@results_bp.route('/')
def get_result():
    db = get_db()
    cur = db.execute("SELECT score FROM tests WHERE user_id = ? ORDER BY id DESC LIMIT 1", (session['id'],))
    result = cur.fetchone()
    if not result:
        return render_template("quizzes.html")
    return render_template("result.html", page="Results", score=result[0])
