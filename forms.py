# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, DateField, validators
from wtforms.validators import Email, Length, InputRequired, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=0, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=0, max=100)])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField("Se connecter")


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Nom', validators=[InputRequired()], render_kw={"placeholder": "Nom"})
    location = StringField('Localisation', validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": "Localisation"})
    email = StringField('Email',
                        validators=[Length(max=100), Email(message='Entrer un email valide.'), InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=100,
                                                                             message='Veuillez mettre un mot de passe plus sécurisé')], render_kw={"placeholder": "Mot de passe"})
    confirm = PasswordField('Confirmer votre mot de passe', validators=[InputRequired(), EqualTo('password',
                                                                                             message='les mots de passe doivent correspondre.')], render_kw={"placeholder": "Confirmation du mot de passe"})

    submit = SubmitField('Soumetre')
