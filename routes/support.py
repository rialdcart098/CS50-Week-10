from flask import Blueprint, render_template, Flask

support_bp = Blueprint('support', __name__, template_folder='../templates/support', url_prefix='/support')

@support_bp.route('/')
def support_home():
    return render_template('support.html', page='Support')