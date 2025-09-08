from flask import Flask, Blueprint, request, jsonify, session
from helpers import get_db, unit_fetch
app = Flask(__name__)

results_bp = Blueprint('results', __name__, template_folder='../templates/results', url_prefix='/results')

@results_bp.route('/', methods=['POST'])
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
            db.execute("INSERT INTO user_progress (questionsDone, questionsCorrect, unit_id) VALUES (?, ?, ?)", (
                amount,
                unitsCorrect[unit],
                unit
            ))
        else:
            db.execute("UPDATE user_progress SET questionsDone = questionsDone + ?, questionsCorrect = questionsCorrect + ? WHERE ")


    db.commit()
    testID = cur.lastrowid
    return jsonify({"status": "ok", "testID": testID })