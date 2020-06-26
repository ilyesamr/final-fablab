# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user, fresh_login_required
from werkzeug.security import generate_password_hash
from app import db
from models import Command, Product, User
from forms import EditProfilForm, EditPassword

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    form = EditProfilForm()
    achats = Command.query.filter(Command.user_id == current_user.id).all()
    achats_id = Command.product_id
    products = Product.query.filter(Product.id == Command.product_id).all()
    return render_template('profil.html', user=current_user, achats=achats, products=products, form=form)


@main.route('/profil/<int:id>', methods=['POST'])
@fresh_login_required
@login_required
def profil_post(id):
    form = EditProfilForm()
    user = User.query.get_or_404(id)
    user.name = form.name.data
    user.location = form.location.data
    db.session.commit()
    flash("Votre compte a été mis a jour !")
    return redirect('/profil')


@main.route('/security/<int:id>', methods=['GET', 'POST'])
@login_required
def security(id):
    form = EditPassword()
    user = User.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        password = generate_password_hash(form.password.data, method='sha256')
        user.password = password
        db.session.commit()
        flash("Votre compte a été mis a jour !")
        return redirect('/profil')
    else:
        return render_template('security.html', user=user, form=form)
