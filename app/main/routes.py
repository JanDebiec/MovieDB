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

