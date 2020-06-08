from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# boutique
@app.route('/boutique')
def boutique():
    return 'Produit'


@app.route('/contact')
def contact():
    return 'contact'

@app.route('/Accueil')
def accueil():
    return 'accueil'

if __name__ == '__main__':
    app.run()
