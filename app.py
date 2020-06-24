# -*- coding: utf-8 -*-
import os
import time
from functools import wraps

import paypalrestsdk
from flask import Flask, render_template, flash, redirect, request, jsonify, abort
from flask_login import LoginManager, login_required, current_user, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.utils import secure_filename
from bdd import db
from models import Product, Cart, Command
from forms import AddProduct, ContactForm, CommandForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Role
from flask_mail import Message, Mail
import requests

mail = Mail()


def create_app():
    app = Flask(__name__)
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AYisym_MP8hcMCBi7LVBhASJjzoPoQlfr13KZUCBdbUECfU7tevm5bvA66TpIdPOf2FZkh2NKqq4ygQL",
        "client_secret": "EKvYU0v5fIzVDTse_NGkXB_5Sbz5rtl35iFkqmy59fAJPNXeMHTAcbU_4JsEAUVK0c-n75nIZkK6dm1A"})
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fablab.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMAGE_UPLOADS"] = 'static/img/uploads'
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
    db.init_app(app)
    with app.app_context():
        db.create_all()

    admin = Admin(app, name='Gestion des stocks', template_mode='bootstrap3')

    # mail part
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'fablab.arras62000@gmail.com'
    app.config["MAIL_PASSWORD"] = 'Fablab1234'

    mail.init_app(app)

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

    def role_required(role_name):
        def decorator(func):
            @wraps(func)
            def authorize(*args, **kwargs):
                if not current_user.has_role(role_name):
                    abort(401)  # not authorized
                return func(*args, **kwargs)

            return authorize

        return decorator

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
        if current_user.has_role(2):
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
    @login_required
    def new_product():
        user = User.query.filter_by(id=current_user.id).first()
        if user.role_id == 2:
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
        else:
            return 'Not allowed'

    @app.route('/panier')
    @login_required
    def panier():
        products_b = Product.query.all()
        products_b_id = Product.id
        products_p = Cart.query.filter_by(product_id=products_b_id, user_id=current_user.id).all()
        products_p_id = Cart.product_id
        products = Product.query.filter(Product.id == products_p_id, Cart.user_id == current_user.id).all()
        if products:
            products_cart = products
            return render_template('panier.html', products=products_cart, products_p=products_p)
        return render_template('panier-vide.html')

    @app.route('/boutique/ajout/<int:id>')
    @login_required
    def new_cart(id):
        product = Product.query.get_or_404(id)
        err_msg = ''
        if product:
            existing_product = Cart.query.filter(Cart.product_id == product.id, Cart.user_id == current_user.id).first()
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

    @app.route('/panier/delete/<int:id>')
    @login_required
    def supp_cart(id):
        product_cart = Cart.query.filter_by(product_id=id).first()
        db.session.delete(product_cart)
        db.session.commit()
        flash('Votre produit a été supprimé !')
        return redirect('/panier')

    @app.route('/panier/update/<int:id>', methods=['POST'])
    @login_required
    def update_cart(id):
        product_cart = Cart.query.filter_by(product_id=id).first()
        product_boutique = Product.query.filter(Product.id == id).first()
        if request.method == 'POST':
            new_quantity = request.form['quantity']
            new_price = float(new_quantity) * product_boutique.price
            product_cart.quantity = new_quantity
            product_cart.total_price = new_price
            db.session.commit()
            flash('Votre produit a été modifié !')
            return redirect('/panier')
        else:
            return redirect('/panier')

    """"
    @app.route('/panier/validate', methods=['GET', 'POST'])
    @login_required
    def validate_cart():
        form = CommandForm
        command_product = Cart.query.filter(Cart.user_id == current_user.id).first()
        if request.method == 'POST':
            if not form.validate():
                flash('Tous les champs sont requis.')
                return render_template('command-informations.html', form=form)
            else:
                user_id = current_user.id
                product_id = command_product.product_id
                user_name = form.name.data
                user_fisrtname = form.firstname.data
                user_email = form.email.data
                user_code = form.code.data
                command_quantity = command_product.quantity
                command_price = int(command_product.total_price)
                new_command = Command(user_id=user_id, product_id=product_id, user_name=user_name,
                                      user_firstname=user_fisrtname, user_email=user_email, user_code=user_code,
                                      command_quantity=command_quantity, command_price=command_price)
                render_template('real-paiement.html', new_command=new_command)
                db.session.add(new_command)
                msg_commande = Message("Nouvelle Commande", sender=form.email.data,
                                       recipients=['fablab.arras62000@gmail.com'])
                mail.send(msg_commande)
                flash('Votre commande est envoyée, elle sera traitée dans le meilleur délai')
                db.session.delete(command_product)
                db.session.commit()
                return render_template('', success=True)
        elif request.method == 'GET':
            return render_template('real-paiement.html', form=form, user=current_user)
    """

    @app.route('/success')
    def success():
        return render_template('success.html')

    @app.route('/panier/paiement')
    @login_required
    def payment():
        command_product = Cart.query.filter_by(user_id=current_user.id).first()
        print(int(command_product.total_price))
        return render_template('paiement.html')

        # return render_template('real-paiement.html', user=current_user, product=command_product,
        # price=int(command_product.total_price))

    """"
    @app.route('/ipn/', methods=['POST'])
    def ipn():
        command_product = Cart.query.filter_by(user_id=current_user.id).first()
        user_id = current_user.id
        product_id = command_product.product_id
        user_email = current_user.email
        user_name = current_user.name
        command_quantity = command_product.quantity
        command_price = int(command_product.total_price)

        new_command = Command(user_id=user_id, product_id=product_id,
                              user_name=user_name,
                              user_firstname='ahmed',
                              user_email=user_email,
                              user_address='Rue winston',
                              user_code=62,
                              command_quantity=command_quantity,
                              command_price=command_price)
        try:
            db.session.add(new_command)
            db.session.delete(command_product)
            db.session.commit()
            msg_command = Message("Nouvelle Commande", sender=user_email,
                                  recipients=['fablab.arras62000@gmail.com'])
            msg_command.html = "<h1>Nouvelle commande</h1>"
            mail.send(msg_command)
            arg = ''
            request.parameter_storage_class = ImmutableOrderedMultiDict
            values = request.form
            for x, y in values.items():
                arg += "&{x}={y}".format(x=x, y=y)

            validate_url = 'https://www.sandbox.paypal.com' \
                           '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                .format(arg=arg)
            r = requests.get(validate_url)

            if r.text == 'VERIFIED':
                try:
                    msg_command = Message("Nouvelle Commande", sender=user_email,
                                          recipients=['fablab.arras62000@gmail.com'])
                    msg_command.html = "<h1>Nouvelle commande</h1>"
                    mail.send(msg_command)
                except Exception as e:
                    return 'error'

            else:
                return 'error'

            return r.text
        except Exception as e:
            return str(e)
    """

    @app.route('/payment', methods=['POST'])
    @login_required
    def payment_new():
        command_product = Cart.query.filter_by(user_id=current_user.id).first()
        price = int(command_product.total_price)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1:5000/payment/execute",
                "cancel_url": "http://127.0.0.1:5000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "testitem",
                        "sku": "12345",
                        "price": price,
                        "currency": "EUR",
                        "quantity": command_product.quantity}]},
                "amount": {
                    "total": price,
                    "currency": "EUR"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print('Payment success!')
        else:
            print(payment.error)

        return jsonify({'paymentID': payment.id})

    @app.route('/execute', methods=['POST'])
    @login_required
    def execute():
        success = False
        command_product = Cart.query.filter_by(user_id=current_user.id).first()
        payment = paypalrestsdk.Payment.find(request.form['paymentID'])

        if payment.execute({'payer_id': request.form['payerID']}):
            print('Execute success!')
            success = True
            user_id = current_user.id
            product_id = command_product.product_id
            user_email = current_user.email
            user_name = current_user.name
            command_quantity = command_product.quantity
            command_price = int(command_product.total_price)
            new_command = Command(user_id=user_id, product_id=product_id,
                                  user_name=user_name,
                                  user_firstname='ahmed',
                                  user_email=user_email,
                                  user_address='Rue winston',
                                  user_code=62,
                                  command_quantity=command_quantity,
                                  command_price=command_price)

            db.session.add(new_command)
            db.session.delete(command_product)
            db.session.commit()
            msg_command = Message("Nouvelle Commande", sender=user_email,
                                  recipients=['fablab.arras62000@gmail.com'])
            msg_command.html = "<h1>Nouvelle commande</h1>"
            mail.send(msg_command)
            return redirect('/achats')
        else:
            print(payment.error)

        return jsonify({'success': success})

    @app.route('/achats')
    @login_required
    def achats():
        achats = Command.query.filter(Command.user_id == current_user.id).all()
        achats_id = Command.product_id
        products = Product.query.filter(Product.id == achats_id).all()
        return render_template('achats.html', achats=achats, products=products)

    @app.route('/mentions')
    def mentions():
        return render_template('mentions.html')

    @app.route('/CGV')
    def CGV():
        return render_template('CGV.html')

    @app.route('/equipe')
    def team():
        return render_template('team.html')

    @app.route('/boutique/<int:id>')
    def details(id):
        product = Product.query.get_or_404(id)
        return render_template('details.html', product=product)

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    app.register_error_handler(404, page_not_found)

    @app.route('/contact', methods=['GET', 'POST'])
    @login_required
    def contact():
        form = ContactForm()
        if request.method == 'POST':
            if not form.validate():
                flash('Tous les champs sont requis.')
                return render_template('contact.html', form=form)
            else:
                msg = Message(form.subject.data, sender=form.email.data, recipients=['fablab.arras62000@gmail.com'])
                msg.body = """
                       De : %s <%s>
                       %s
                       """ % (form.name.data, form.email.data, form.message.data)
                mail.send(msg)
                return render_template('contact.html', success=True)
        elif request.method == 'GET':
            return render_template('contact.html', form=form, user=current_user)

    @app.route('/boutique/<int:id>')
    def detail(id):
        product = Product.query.get_or_404(id)
        return render_template('detail.html', product=product)

    return app
