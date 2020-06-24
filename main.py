from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from models import Command, Product, User
from forms import EditProfilForm

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
    products = Product.query.filter(Product.id == achats_id).all()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        user.name = form.name.data
        user.location = form.location.data
        db.session.commit()
        flash("Votre compte a été mis a jour !")
        return redirect('/profil')
    else:
        return render_template('profil.html', user=current_user, achats=achats, products=products, form=form)
