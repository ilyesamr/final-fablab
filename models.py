from functools import wraps
from os import abort

from flask_login import UserMixin, current_user
from datetime import datetime
from bdd import db


def instock(var):
    if var > 0:
        return True
    return False


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

    def has_roles(self, *args):
        return set(args).issubset({role.description for role in self.role_id})

    def has_role(self, role):
        return role in self.role_id

    def is_accessible(self):
        if self.role_id == 2:
            return True
        else:
            return False


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.description


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    inStock = db.Column(db.Boolean, nullable=True)
    cart = db.relationship('Cart', backref='product')
    comments = db.relationship('Comment', backref='product', lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "Comment('{self.body}', '{self.timestamp}')"


class Cart(db.Model):
    __tablename__ = 'cart'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.DECIMAL)

    def __repr__(self):
        return "Cart('{self.user_id}', '{self.product_id}, '{self.quantity}')"


class Command(db.Model):
    __tablename__ = 'commands'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    user_name = db.Column(db.String, nullable=False)
    user_firstname = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_address = db.Column(db.String(50), nullable=False)
    user_code = db.Column(db.Integer)
    command_quantity = db.Column(db.Integer, nullable=False)
    command_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Command %r>' % self.name
