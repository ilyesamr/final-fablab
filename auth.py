# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User
from forms import LoginForm, SignupForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        email = form.email.data
        password = form.password.data
        remember = True if form.remember.data else False
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.profil'))
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Adresse mail dèjà prise ! ')
            return redirect(url_for('auth.signup'))
        new_user = User(name=form.name.data, location=form.location.data, email=form.email.data, password=generate_password_hash(form.password.data, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Votre compte a été créé avec succès')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


