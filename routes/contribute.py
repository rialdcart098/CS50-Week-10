from flask import Flask, Blueprint, render_template

contribute_bp = Blueprint('contribute', __name__, template_folder='../templates/contribute', url_prefix='/contribute')

@contribute_bp.route('/')
def contribute_home():
    return render_template('contribute.html', page='Contribute')