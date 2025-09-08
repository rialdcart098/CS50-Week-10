from flask import Flask, Blueprint, request, jsonify, session, render_template, redirect
from helpers import login_required
from helpers import get_db, unit_fetch
app = Flask(__name__)

results_bp = Blueprint('results', __name__, template_folder='../templates/results', url_prefix='/results')

@results_bp.route('/', methods=['POST'])
@login_required
def results():
    results = request.get_json()
    totalQuestion = results['totalQuestion']
    correctAnswers = results['correctAnswers']
    score = (correctAnswers / totalQuestion) * 100
    db = get_db()
    cur = db.execute("INSERT INTO tests (user_id, test, score, subject_id) VALUES (?, ?, ?, ?)", (
        session['id'],
        results['exam'],
        score,
        results['subject']
    ))
    unitsDone = results['units']
    unitsCorrect = results['unitsCorrect']
    for unit, amount in enumerate(unitsDone):
        if unit_fetch(unit) <= 0:
            db.execute("INSERT INTO user_progress (questionsDone, questionsCorrect, unit_id, user_id) VALUES (?, ?, ?, ?)", (
                amount,
                unitsCorrect[unit],
                unit,
                session['id']
            ))
        else:
            db.execute("UPDATE user_progress SET questionsDone = questionsDone + ?, questionsCorrect = questionsCorrect + ? WHERE unit = ? AND user_id = ?", (
                amount,
                unitsCorrect[unit],
                unit,
                session['id']
            ))


    db.commit()
    testID = cur.lastrowid
    return jsonify({"status": "ok", "testID": testID })

@results_bp.route('/<int:testID>')
@login_required
def result_page(testID):
    db = get_db()
    cur = db.execute("SELECT * FROM tests WHERE id = ?", (
        testID,)).fetchone()
    if not cur:
        return redirect('/quizzes')
    return render_template('results.html', testName=cur[2] score=cur[3], page="Results")