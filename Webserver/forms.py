import sys, os
sys.path.append(os.path.dirname(__file__))

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Email
from werkzeug.security import generate_password_hash

#login
class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Einloggen')

#Password recovery
class RecoveryForm(FlaskForm):
    email = StringField('Email', validator=[InputRequired(), Email(check_deliverability=True)])
    submit = SubmitField('Registrieren')

class PasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[InputRequired(), EqualTo('password_confirm', message="Die Passwörter müssen übereinstimmen")])
    password_confirm = PasswordField('Passwort wiederholen')
    submit = SubmitField('Registrieren')

#registration
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=5, max=255)])
    password = PasswordField('Passwort', validators=[InputRequired(),
                                        EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')
    accept_tos = BooleanField('Hiermit bestätige ich die AGBs gelesen und akzeptiert zu haben', validators=[InputRequired()])
    submit = SubmitField('Registrieren')

#creating a new entry
class EntryForm(FlaskForm):
    title = StringField('Titel', validator=[InputRequired(), Length(max=100)])
    description = StringField('Bitte beschreiben sie das Produkt', validator=[InputRequired(), Length(min=30, max=1500)])
    img_1 = FileField()
    img_2 = FileField()
    img_3 = FileField()
    img_4 = FileField()
    submit = SubmitField('Artikel einstellen')

