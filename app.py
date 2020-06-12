from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fablab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db

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


@app.route('/boutique')
def boutique():
    return render_template('boutique.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/mentions')
def mentions():
    return render_template('mentions.html')


if __name__ == '__main__':
    app.run(debug=True)
