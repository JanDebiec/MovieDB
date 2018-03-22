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
    # nameB = 'AMG'
    nameB = comparedir['B']

    comparison = Comparison(nameA, nameB)
    resultComp = comparison.compare()

    # criticA is reserved for owner

    criticBObj = Critic.query.filter_by(name=nameB).first()
    criticBObj.simdistance = resultComp.distance
    criticBObj.simpearson = resultComp.pearson
    db.session.commit()

    resultComp.best_fit()
    points = resultComp.generate_line_points()


    labels = [nameA, nameB]
    legend = "critics compare"
    return render_template('mod_critics/results.html',
                           title='Result of compare Critics',
                           form=form,
                           values=resultComp.listForChart,
                           labels=labels,
                           legend=legend,
                           points= points,
                           result = resultComp
                           )
    # return render_template('mod_critics/chart.html',
    #                        values=result.listForChart, labels=labels, legend=legend)

@mod_critics.route("/init_mc")
def init_mc():
    '''
    for movies, which have JD or AMG ratings,
    scrap the metacritics for the film.
    Insert the ratings in db.
    Schow the results
    Then go to template to calculate similarity of critics
    :return:
    '''
    pass

@mod_critics.route("/calc_mc")
def calc_mc():
    pass

@mod_critics.route("/chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January","February","March","April","May","June","July","August"]
    # values = [10,9,8,7,6,4,7,8]
    values = [
        (10,
               9
         ),(
       4,
       7
        ), (
            9,
       9
        ), (
            3,
       8
        ), (
            2,
       4
        ), (
            8,
       7
        ), (
            1,
       3
        ), (
            4,
       5
        )]
    return render_template('mod_critics/chart.html',
                           values=values, labels=labels, legend=legend)

