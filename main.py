from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/profil')
@login_required
def profil():
    return render_template('profil.html', user=current_user)
