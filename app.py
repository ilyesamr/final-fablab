from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fablab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/boutique')
def boutique():
    return render_template('boutique.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/mention')
def mention():
    return render_template('mention.html')

@app.route('/CGV')
def CGV():
    return render_template('CGV.html')

if __name__ == '__main__':
    app.run(debug=True)
