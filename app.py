# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, flash, redirect, request
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from bdd import db
from models import Product, Cart
from forms import AddProduct
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Role


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fablab.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMAGE_UPLOADS"] = 'static/img/uploads'
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
    db.init_app(app)

    with app.app_context():
        db.create_all()

    admin = Admin(app, name='Gestion des utilisateurs', template_mode='bootstrap3')

    # verification de l'extenstion de l'image
    def allowed_image(filename):
        # des images avec un point seulement
        if not "." in filename:
            return False

        # split l'extenstion du nom de l'image
        ext = filename.rsplit(".", 1)[1]

        # on vérifie que l'extension est bonne
        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False

    def instock(var):
        if var > 0:
            return True
        return False

    # login part
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Cart, db.session))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/boutique', methods=['GET', 'POST'])
    def boutique():
        form = AddProduct()
        if form.validate_on_submit() and request.method == 'POST':
            product_name = form.name.data
            product_description = form.description.data
            product_image = form.image.data
            product_price = form.price.data
            product_quantity = form.quantity.data
            product_instock = form.inStock.data
            if allowed_image(product_image.filename):
                filename = secure_filename(product_image.filename)
                product_image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
                new_product = Product(name=product_name, description=product_description,
                                      image=filename, price=product_price, quantity=product_quantity,
                                      inStock=product_instock)
                db.session.add(new_product)
                db.session.commit()
                flash('Votre produit a été ajouté')
                return redirect('/boutique')
        all_products = Product.query.all()
        role_admin = 2
        return render_template('boutique.html', products=all_products, form=form, user=current_user,
                               role_admin=role_admin)

    @app.route('/boutique/new', methods=['GET', 'POST'])
    def new_product():
        form = AddProduct()
        if form.validate_on_submit() and request.method == 'POST':
            product_name = form.name.data
            product_description = form.description.data
            product_image = form.image.data
            product_price = form.price.data
            product_quantity = form.quantity.data
            product_instock = form.inStock.data
            if allowed_image(product_image.filename):
                filename = secure_filename(product_image.filename)
                product_image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
                new_product = Product(name=product_name, description=product_description,
                                      image=filename, price=product_price, quantity=product_quantity,
                                      inStock=product_instock)
                db.session.add(new_product)
                db.session.commit()
                flash('Votre produit a été ajouté')
                return redirect('/boutique')
        else:
            return render_template('boutique-new.html', form=form)

    @app.route('/panier')
    def panier():
        products_b = Product.query.all()
        products_b_id = Product.id
        products_p = Cart.query.filter_by(product_id=products_b_id).all()
        products_p_id = Cart.product_id
        products = Product.query.filter(Product.id == products_p_id, Cart.user_id == current_user.id).all()
        if products:
            products_cart = products
            return render_template('panier.html', products=products_cart)
        return render_template('panier-vide.html')

    @app.route('/boutique/ajout/<int:id>')
    @login_required
    def new_cart(id):
        product = Product.query.get_or_404(id)
        err_msg = ''
        if product:
            existing_product = Cart.query.filter_by(product_id=product.id).first()
            if not existing_product:
                new_product_cart = Cart(user_id=current_user.id, product_id=product.id, quantity=1,
                                        total_price=product.price)
                db.session.add(new_product_cart)
                db.session.commit()
                flash("Produit ajouté !")
                return redirect('/panier')
            else:
                err_msg = 'Le produit existe dèjà dans le panier'

        if err_msg:
            flash(err_msg)
            return redirect('/boutique')

    @app.route('/panier/paiement')
    @login_required
    def paiement():
        return render_template('paiement.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/mentions')
    def mentions():
        return render_template('mentions.html')

    @app.route('/CGV')
    def CGV():
        return render_template('CGV.html')

    return app
