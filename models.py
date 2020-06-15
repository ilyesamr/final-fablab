from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    inStock = db.Column(db.Boolean, nullable=False, default=True)
    comments = db.relationship('Comment', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"


class Command(db.Model):
    __tablename__ = 'commands'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    user_name = db.Column(db.String, nullable=False)
    user_firstname = db.Column(db.String, nullable=False)
    user_address = db.Column(db.String(50), nullable=False)
    user_code = db.Column(db.Integer)
    command_quantity = db.Column(db.Integer, nullable=False)
    command_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Command %r>' % self.name


class SaleTransaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    command_id = db.Column(db.Integer, db.ForeignKey('command.id'), nullable=False)

    transaction_date = db.Column(db.DateTime, nullable=False)

    amount = db.Column(db.DECIMAL, nullable=False)

    cc_number = db.Column(db.String(50), nullable=False)

    cc_type = db.Column(db.String(50), nullable=False)

    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Order('{self.transactionid}', '{self.orderid}','{self.transactiondate}','{self.amount}', '{self.cc_number}','{self.cc_type}','{self.response}')"
