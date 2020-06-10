from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, TextAreaField, DateField, validators
from wtforms.validators import Email, Length, InputRequired, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Votre mail', validators=[InputRequired(), Length(min=0, max=20)])
    password = PasswordField('Votre mot de passe', validators=[InputRequired(), Length(min=0, max=100)])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField("Se connecter")


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('name', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email',
                        validators=[Length(max=100), Email(message='Entrer un email valide.'), InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=100,
                                                                             message='Veuillez mettre un mot de passe plus sécurisé')])
    confirm = PasswordField('confirmer votre password', validators=[InputRequired(), EqualTo('password',
                                                                                             message='les mots de passe doivent correspondre.')])

    submit = SubmitField('Valider')
