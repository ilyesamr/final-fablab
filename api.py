from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
import json
from app import ma, db
from models import User, Product
import warnings
from marshmallow_sqlalchemy import ModelSchema

with warnings.catch_warnings():
    from flask_marshmallow import Marshmallow

api = Blueprint('api', __name__)


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "quantity")


# Product Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "location", "email")


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Create a Product
@api.route('/api/adduser/', methods=['POST'])
def add_user():
    name = request.json['name']
    location = request.json['location']
    email = request.json['email']
    password = request.json['password']
    new_user = User(name=name, location=location, email=email,
                    password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


@api.route("/api/users/", methods=['GET'])
def users():
    users_all = User.query.all()
    result = users_schema.dump(users_all)
    return json.dumps(result)


# Update a User
@api.route("/api/users/<id>", methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    name = request.json['name']
    location = request.json['location']
    email = request.json['email']
    password = request.json['password']
    user.name = name
    user.location = location
    user.email = email
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    return user_schema.jsonify(user)


# Delete User
@api.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


# Get All Products
@api.route('/api/products/', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get Single Products
@api.route('/api/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a Product
@api.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)


# Delete Product
@api.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

