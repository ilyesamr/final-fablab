# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, DateField, validators, \
    DecimalField, FileField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=0, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=0, max=100)])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField("Se connecter")


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Nom', validators=[InputRequired()])
    location = StringField('Localisation', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email',
                        validators=[Length(max=100), Email(message='Entrer un email valide.'), InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=100,
                                                                                 message='Veuillez mettre un mot de passe plus sécurisé')])
    confirm = PasswordField('Confirmer votre mot de passe', validators=[InputRequired(), EqualTo('password',
                                                                                                 message='les mots de passe doivent correspondre.')])

    submit = SubmitField('Soumetre')


class AddProduct(FlaskForm):
    name = StringField('Nom', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(max=200)])
    image = FileField('Image', validators=[FileRequired()])
    price = DecimalField('Prix', validators=[InputRequired()])
    inStock = BooleanField('En stock', validators=[InputRequired()])
    quantity = IntegerField('Quantité', validators=[InputRequired()])

    submit = SubmitField('Ajouter')


class AddCommentForm(FlaskForm):
    body = StringField("Body", validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField("Publier")
