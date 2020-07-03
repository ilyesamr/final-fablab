# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, DateField, validators, \
    DecimalField, FileField, IntegerField
from wtforms.validators import Email, Length, InputRequired, EqualTo, DataRequired, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=20)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=0, max=100)])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField("Se connecter")


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Nom, prénom', validators=[InputRequired()])
    location = StringField('Adresse', validators=[InputRequired(), Length(max=50)])
    email = StringField('Email',
                        validators=[Length(max=100), Email(message='Entrer un email valide.'), InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=8, max=100,
                                                                                 message='Veuillez mettre un mot de '
                                                                                         'passe plus sécurisé')])
    confirm = PasswordField('Confirmer votre mot de passe', validators=[InputRequired(), EqualTo('password',
                                                                                                 message='les mots de '
                                                                                                         'passe '
                                                                                                         'doivent '
                                                                                                         'correspondre.')])
    accept = BooleanField('Accepter les conditions générales de ventes', validators=[DataRequired(message="Vous devez "
                                                                                                          "accepter "
                                                                                                          "nos "
                                                                                                          "conditions "
                                                                                                          "pour "
                                                                                                          "pouvoir "
                                                                                                          "vous "
                                                                                                          "inscrire")])
    submit = SubmitField('Soumettre')


class AddProduct(FlaskForm):
    name = StringField('Nom', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(max=1000)])
    image = FileField('Image', validators=[FileRequired()])
    price = DecimalField('Prix', validators=[InputRequired()])
    inStock = BooleanField('En stock', validators=[InputRequired()])
    quantity = IntegerField('Quantité', validators=[InputRequired()])

    submit = SubmitField('Ajouter')


class AddCommentForm(FlaskForm):
    body = StringField("Body", validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    submit = SubmitField("Publier")


class ContactForm(FlaskForm):
    name = StringField("Nom", [validators.DataRequired("Veuillez entrer votre nom.")])
    email = StringField("Email", [validators.DataRequired("Veuillez entrer votre e-mail."), validators.Email()])
    subject = StringField("Objet", [validators.DataRequired("Veuillez entrer l'objet.")])
    message = TextAreaField("Message", [validators.DataRequired("Veuillez entrer le message.")])
    submit = SubmitField("Envoyer")


class CommandForm(FlaskForm):
    name = StringField("Nom", [validators.DataRequired("Veuillez entrer votre nom.")])
    firstname = StringField("Prénom", [validators.DataRequired("Veuillez entrer votre prénom.")])
    email = StringField("Email", [validators.DataRequired("Veuillez entrer votre e-mail."), validators.Email()])
    address = StringField("Adresse", [validators.DataRequired("Veuillez entrer votre adresse.")])
    code = IntegerField('Code postale', validators=[InputRequired()])
    submit = SubmitField("Valider la commande")


class EditProfilForm(FlaskForm):
    name = StringField('Nom complet', validators=[InputRequired(), Length(3, 64)])
    location = StringField("Adresse", validators=[validators.DataRequired("Veuillez entrer votre adresse.")])
    submit = SubmitField("Confirmer les modifications")


class EditPassword(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[InputRequired(), Length(min=8, max=100,
                                                                                 message='Veuillez mettre un mot de '
                                                                                         'passe plus sécurisé')])
    confirm = PasswordField('Confirmer votre nouveau mot de passe', validators=[InputRequired(), EqualTo('password',
                                                                                                 message='les mots de '
                                                                                                         'passe '
                                                                                                         'doivent '
                                                                                                         'correspondre.')])
    submit = SubmitField("Changer le mot de passe")