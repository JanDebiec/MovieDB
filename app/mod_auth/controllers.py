import os
import sys
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

mod_auth = Blueprint('auth', __name__, url_prefix='/mod_auth')

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
