from flask import render_template
# from app import current_app
from app.main import bp

# @app.route('/')
# @app.route('/index')
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')

@bp.route('/userinput/maninput', methods=['GET', 'POST'])
def maninput():
    return render_template('userinput/maninput.html',
                           title='Manual Input')

@bp.route('/userinput/csvinput', methods=['GET', 'POST'])
def csvinput():
    return render_template('userinput/csvinput.html',
                           title='CSV Input')
