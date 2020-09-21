import sys, os
sys.path.append(os.path.dirname(__file__))

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Email
from werkzeug.security import generate_password_hash

class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Einloggen')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=5, max=255)])
    password = PasswordField('Passwort', validators=[InputRequired(),
                                        EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')
    accept_tos = BooleanField('Hiermit bestätige ich die AGBs gelesen und akzeptiert zu haben', validators=[InputRequired()])
    submit = SubmitField('Registrieren')

class RecoveryForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validator=[InputRequired()])
    submit = SubmitField('Registrieren')

class EntryForm(FlaskForm):
    title = StringField('Titel', validator=[InputRequired(), Length(max=100)])
    description = StringField('Bitte beschreiben sie das Produkt', validator=[InputRequired(), Length(min=30, max=1500)])

    submit = SubmitField('Artikel einstellen')