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
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    InStock = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Product %r>' % self.name

class Command(db.Model):
    __tablename__ = 'commands'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    user_address = db.Column(db.String(50))
    command_quantity = db.Column(db.Integer, nullable=False)
    command_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Command %r>' % self.name