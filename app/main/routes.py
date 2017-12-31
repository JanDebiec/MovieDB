from flask import render_template, flash, redirect
# from app import current_app
from app.main import bp
from app.userinput import bp as usibp
from app.userinput.forms import ManInputForm

# @app.route('/')
# @app.route('/index')
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')

@bp.route('/userinput/maninput', methods=['GET', 'POST'])
def maninput():
    form = ManInputForm()
    if form.validate_on_submit():
        flash('Added Movie: Id={}, localName={}, medium={}'.format(
            form.imdbid.data, form.localname.data, form.medium.data
        ))
        return redirect('/index')
    return render_template('userinput/maninput.html',
                           title='Manual Input',
                           form=form)

@bp.route('/userinput/csvinput', methods=['GET', 'POST'])
def csvinput():
    return render_template('userinput/csvinput.html',
                           title='CSV Input')
