import os
import sys
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app.mod_db.models import User
from app.mod_auth.forms import LoginForm

mod_auth = Blueprint('auth', __name__, url_prefix='/mod_auth')

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('mod_auth/login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('mod_auth/login.html', title='Sign In', form=form)

@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))