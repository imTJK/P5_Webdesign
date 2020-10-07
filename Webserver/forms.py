import sys, os
sys.path.append(os.path.dirname(__file__))

from Webserver import app
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Email
from werkzeug.security import generate_password_hash
from wtforms.fields.core import SelectField
from wtforms.widgets.core import TextArea


SECURITY_QUESTIONS =  [(0, 'Wie hieß dein erstes Haustier?'),(1, 'Straße, in der Sie als Kind gewohnt haben?'), (2, 'Bester Freund in Ihrer Kindheit?'), (3, 'Vorname Ihres Großvaters?')]

#login
class LoginForm(FlaskForm):
    email_username = StringField('Email oder Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Einloggen')

#for 2fa
class TokenForm(FlaskForm):
    token = StringField('Token', validators=[InputRequired(), Length(6, 6)], render_kw={"placeholder": "Ihr TOTP-Token"})
    submit = SubmitField('Bestätigen')

#email-confirmation Form 
class ConfirmForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    submit = SubmitField('Bestätigen')

#Password-Recovery Form
class RecoveryForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    security_question = SelectField(u'Bitte wählen sie ihre Sicherheitsfrage aus', choices = SECURITY_QUESTIONS, validators = [InputRequired()])
    security_answer = StringField('Ihre Antwort', validators=[InputRequired()])
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
    

    security_question = SelectField(u'Bitte wählen sie eine Sicherheitsfrage aus', choices = SECURITY_QUESTIONS, validators = [InputRequired()])
    security_answer = StringField('Antwort', validators=[InputRequired()])
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
    username = StringField('Benutzername', validators=[Length(min=5, max=255)])
    
    #current Password, not changed
    password = PasswordField('Neues Passwort', validators=[EqualTo('confirm', message="Passwörten müssen übereinstimmen")])
    confirm = PasswordField('Passwort wiederholen')

    submit = SubmitField('Speichern')

#redirect-Form for edit-Pages
class EditForm(FlaskForm):
    submit = SubmitField('Bearbeiten')

class SubmitForm(FlaskForm):
    submit = SubmitField('Bestätigen')

class SearchForm(FlaskForm):    
    term = StringField(label='', validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Was suchen sie?"}) #identical validators to Entry-Title 

class MessageForm(FlaskForm):
    message = StringField('Message...', validators=[InputRequired(), Length(min=20)], widget=TextArea(), render_kw={"placeholder": "Nachricht..."})
    submit = SubmitField()

class DeletionForm(FlaskForm):
    confirm = BooleanField('Sind sie sich sicher?', validators=[InputRequired()])
    submit = SubmitField()

class TwoFactorDeletionForm(FlaskForm):
    confirm = BooleanField('Sind sie sich sicher?', validators=[InputRequired()])
    token = StringField('Token', validators=[InputRequired(), Length(6, 6)], render_kw={"placeholder": "Ihr TOTP-Token"})
    submit = SubmitField('Bestätigen')