from flask import Blueprint, render_template, flash, redirect, url_for
# from app import current_app

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET', 'POST'])
@mod_main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Home')

