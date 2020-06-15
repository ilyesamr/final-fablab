import os

from flask import Flask, render_template, flash, redirect, request
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from bdd import db
from models import Product
from forms import AddProduct

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fablab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["IMAGE_UPLOADS"] = 'static/img/uploads'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
db.init_app(app)


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
    return render_template('boutique.html', products=all_products, form=form)


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
@login_required
def panier():
    return render_template('panier.html')


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


if __name__ == '__main__':
    app.run(debug=True)
