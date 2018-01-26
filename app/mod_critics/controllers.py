import json
from flask import Blueprint, render_template, flash, redirect, url_for
import csv

from config import Config

import helper as h
import app.mod_imdb.controllers as tsv

from app import db
from app.mod_db.models import Movie, Role, People, Director, Critic
from app.mod_critics.forms import CompareCriticsForm, CompareResultsForm

from app.mod_critics.functions import *


mod_critics = Blueprint('critics', __name__, url_prefix='/mod_critics')

@mod_critics.route('/compare', methods=['GET', 'POST'])
def compare():
    form = CompareCriticsForm()
    if form.validate_on_submit():
        comparedir = {}
        comparedir['A'] = form.critica.data
        comparedir['B'] = form.criticb.data
        compareitems = json.dumps(comparedir)
        return redirect(url_for('critics.results',compareitems=compareitems ))


    return render_template('mod_critics/compare.html',
                           title='Compare Critics',
                           form=form,
                           )


@mod_critics.route('/results/<compareitems>', methods=['GET', 'POST'])
def results(compareitems):
    form = CompareResultsForm()
    comparedir = json.loads(compareitems)
    nameA = 'JD'
    # nameA = comparedir['A']
    nameB = 'AMG'
    # nameB = comparedir['B']
    # result = 17.8
    comparison = Comparison(nameA, nameB)
    result = comparison.calcCompare()
    return render_template('mod_critics/results.html',
                           title='Result of compare Critics',
                           form=form,
                           result = result
                           )

