import sys, os
sys.path.append(os.path.dirname(__file__))

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Email
from werkzeug.security import generate_password_hash

#login
class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Einloggen')

#email-confirmation Form (used for password recovery)
class RecoveryForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    submit = SubmitField('Bestätigen')

#Password-reset Form 
class PasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[InputRequired(), EqualTo('password_confirm', message="Die Passwörter müssen übereinstimmen")])
    password_confirm = PasswordField('Passwort wiederholen')
    submit = SubmitField('Bestätigen')

#registration
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    username = StringField('Benutzername', validators=[InputRequired(), Length(min=5, max=255)])
    password = PasswordField('Passwort', validators=[InputRequired(),
                                        EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')
    accept_tos = BooleanField('Hiermit bestätige ich die AGBs gelesen und akzeptiert zu haben', validators=[InputRequired()])
    submit = SubmitField('Registrieren')

#Entry-Form 2-Parter consisting of Body and Images seperately
class EntryBody(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(max=100)])
    description = StringField('Bitte beschreiben sie das Produkt', validators=[InputRequired(), Length(min=30, max=1500)])

class EntryImages(FlaskForm):
    img_1 = FileField('Haupt-Bild',validators=[FileRequired()])
    img_2 = FileField('Bild 2')
    img_3 = FileField('Bild 3')
    img_4 = FileField('Bild 4')

#create new Entry
class EntryForm(EntryBody, EntryImages):
    submit = SubmitField('Artikel einstellen')

class EntryEditForm(EntryBody, EntryImages):
    # wack
    submit = SubmitField('Änderungen speichern')

class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[Email(check_deliverability=True)])
    username = StringField('Benutzername', validators=[Length(min=5, max=255)])
    
    #current Password, not changed
    password = PasswordField('Neues Passwort', validators=[EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')

    submit = SubmitField('Speichern')
    confirm_submit = BooleanField('Bist du dir sicher?')

#redirect-Form for edit-Pages
class EditForm(FlaskForm):
    submit = SubmitField('Bearbeiten')

class SearchForm(FlaskForm):    
    term = StringField('Wonach suchen sie?', validators=[InputRequired(), Length(max=100)]) #identical validators to Entry-Title 
    submit = SubmitField('Suchen')