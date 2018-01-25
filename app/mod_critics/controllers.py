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
    return render_template('mod_critics/compare.html',
                           title='Compare Critics',
                           form=form,
                           )
