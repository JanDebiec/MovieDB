from flask import Blueprint, render_template, flash, redirect, url_for

from app import db
from app.userinput.forms import ManInputForm, CsvInputForm

mod_input = Blueprint('input', __name__, url_prefix='/userinput')

@mod_input.route('/maninput', methods=['GET', 'POST'])
def maninput():
    form = ManInputForm()
    if form.validate_on_submit():
        flash('Added Movie: Id={}, localName={}, medium={}'.format(
            form.imdbid.data, form.localname.data, form.medium.data
        ))
        insertManualInput(form)
        return redirect('/index')
    return render_template('userinput/maninput.html',
                           title='Manual Input',
                           form=form)


@mod_input.route('/csvinput', methods=['GET', 'POST'])
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

def checkDataFromCsv():
    '''
    read CSV file from file system,
    for every line get the data record,
    check if movie alredy listed in db
    and insert/update the db (with the help of db module
    '''
    pass

def insertManualInput(manInputForm):
    ''' extract data from InputForm,
    validate and insert/update in db
    '''
    imdbid = manInputForm.imdbid.data
    localname = manInputForm.localname.data
    medium = manInputForm.medium.data

    flash('Added Movie: Id={}, localName={}, medium={}'.format(
        imdbid, localname, medium
    ))
    # dbData = dbh.insertMovieData(imdbid, localname, medium)
    pass

