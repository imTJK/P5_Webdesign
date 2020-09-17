from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Einloggen')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(),
                                        EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')
    accept_tos = BooleanField('Hiermit bestätige ich die AGBs gelesen und akzeptiert zu haben', validators=[DataRequired()])