import sys, os
sys.path.append(os.path.dirname(__file__))

### local imports
from Webserver import app, login_manager, db
from Webserver.forms import LoginForm, RegistrationForm, RecoveryForm
from Webserver.cursor import Cursor
from Webserver.mailserver import Email
from Webserver.models import User, Entry

### package imports
from flask import render_template, abort, url_for, request, session, redirect
from flask_login import current_user, login_required, login_user, logout_user
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from _datetime import timedelta


def flash_errors(form):
    if form:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"%s - %s" %(
                    getattr(form, field).label.text,
                    error
                ))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.ALLOWED_EXTENSIONS

#login_manager to handle User-specific Requests
@login_manager.user_loader
def load_user(id):
    #int-cast due to flask_login passing ids as Strings
    return User.query.get(int(id)) 

#login-required callback
@login_manager.unauthorized_handler
def unauthorized_user():
    return redirect(url_for('login'))

###   Routing   ###
@app.route('/homepage', methods=['GET'])
def homepage():
    return render_template('homepage.html', css_link=url_for('static', filename='css/homepage.css')) 
    #css_link css und anwendung von html-vererbung zusammen mit Jinja2 Variablen

@app.route('/terms-of-service', methods=['GET'])
def tos():
    #Terms of Service / Allgemeine Geschäftsbedingungen
    #nicht unbedingt notwendig
    pass

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = RegistrationForm(request.form)
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() and  User.query.filter_by(email=form.email.data).first():
            form.username.errors('Nutzername und E-Mail werden bereits für einen account verwendet')
            return redirect(url_for('register'))
        elif User.query.filter_by(username=form.username.data).first() is not None:
            form.username.errors.append('Benutzername bereits vergeben')
            return redirect(url_for('register'))
        elif User.query.filter_by(email=form.email.data).first() is not None:
            form.email.errors.append('Ein Nutzer mit der E-Mail-Adresses ist bereits registriert')
            return redirect(url_for('register'))
        else:
            user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('homepage'))
    elif not form.validate_on_submit():
        flash_errors(form)
        return render_template('register.html', title='Registrieren', form=form, css_link=url_for('static', filename='css/homepage.css'))
    
    return render_template('register.html', title='Registrieren', form=form, css_link=url_for('static', filename='css/homepage.css'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    #still to be added:
        #a function against brute force attacks - possibly cookie that logs log in attempts and stops them after 5 tries and resets every 30mins or so
            #possibly a captcha/OAuth-Integration
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm(request.form)
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.email_username.data).first()
        ##workaround for being able to use both the username and email to login with
        if user == None:
            user = User.query.filter_by(email=form.email_username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Falsche Login-Daten')
                return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(days=10))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            #netloc checks wether the page has a different domain-name then the one of our application / if the url is relative
            return redirect(url_for('homepage'))
        return redirect(next_page)
    elif request.method == 'POST' and not form.validate_on_submit():
        flash_errors(form)

    return render_template('login.html', title='Login', form=form, css_link=url_for('static', filename='css/homepage.css'))
        

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/recover', methods=['POST', 'GET'])
def recover_account():
        #password recovery
        #checks if e-mail is in database and sends a customized link to it
        #approach:
            #send hashed e-mail as link to recover/(hashed-mail-goes-here)
            #let the user re-enter their e-mail in order to avoid people getting their link through wireshark or smth like it
            #new cursor form for edit_password
        pass

@app.route('/recover/<recovery_id>', methods=['POST', 'GET'])
def confirm_recovery(recovery_id):
    #recovery_id = hashed e-mail of user
    #let user re-enter their e-mail, use check_password_hash
    #edit_password WTForm
    pass

@app.route('/entry/new-Entry', methods=['POST', 'GET'])
@login_required
def new_entry():
    abort(401)

@app.route('/entry/<int:entry_id>',  methods=['GET'])
def show_entry(entry_id):
    abort(401)

@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def account_page(user_id):
    abort(401)

@app.route('/', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Keine Datei ausgewählt')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            with open(filename, 'rb') as file:
                blob = file.read()
            