from flask import Flask, Blueprint, redirect, session

app = Flask(__name__)

results_bp = Blueprint('results', __name__, template_folder='../templates/results', url_prefix='results')

@results_bp.route('/')
def results():
    return redirect('results.html')