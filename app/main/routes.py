from flask import render_template, flash, redirect, url_for
# from app import current_app
from app.main import bp
from app.userinput import bp as usibp
import app.userinput as usih
from app.userinput.forms import ManInputForm, CsvInputForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')


@bp.route('/userinput/maninput', methods=['GET', 'POST'])
def maninput():
    form = ManInputForm()
    if form.validate_on_submit():
        # flash('Added Movie: Id={}, localName={}, medium={}'.format(
        #     form.imdbid.data, form.localname.data, form.medium.data
        # ))
        usih.insertManualInput(form)
        return redirect('/index')
    return render_template('userinput/maninput.html',
                           title='Manual Input',
                           form=form)


@bp.route('/userinput/csvinput', methods=['GET', 'POST'])
def csvinput():
    form = CsvInputForm()
    if form.validate_on_submit():
        flash('File choosen: {}'.format(
            form.filename.data
        ))
        return redirect('/index')
    return render_template('userinput/csvinput.html',
                           title='CSV Input',
                           form=form)

