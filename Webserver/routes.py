import sys, os
sys.path.append(os.path.dirname(__file__))

from flask import render_template, abort, url_for, request, session, redirect
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from Webserver import app, login_manager
from Webserver.forms import LoginForm, RegistrationForm
from Webserver.cursor import Cursor
from Webserver.mailserver import Email
from Webserver.models import User, Entry
from _datetime import timedelta


#MariaDB-Integration
cur = None
@app.before_first_request
def before_first_request():
    global cur
    cur = Cursor('mariadbtest', 'password', 'localhost', 3306, 'p5_database')

@login_manager.user_loader
def load_user(id):
    #int-cast due to flask_login passing ids as Strings
    return User.get.query(int(id)) 

#Routing
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    user = {'username' : 'Hassan'}
    return render_template('index.html', user=user, css_link=url_for('static', filename='css/index.css')) 
    #css_link css und anwendung von html-vererbung zusammen

@app.route('/terms-of-service', methods=['GET'])
def tos():
    #Terms of Service / Allgemeine Geschäftsbedingungen
    #nicht unbedingt notwendig
    pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email_username.data).first()
        if user == None:
            user = User.query.filter_by(email=form.email_username.data).first()
        
            
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        pass
    abort(401)

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