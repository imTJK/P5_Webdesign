from flask import render_template, abort, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from Webserver import app, login_manager
from Webserver.forms import LoginForm, RegistrationForm
from Webserver.cursor import Cursor
from Webserver.mailserver import Email
from _datetime import timedelta


#MariaDB-Integration
cur = None
@app.before_first_request
def before_first_request():
    global cur
    cur = Cursor('mariadbtest', 'password', 'localhost', 3306, 'p5_database')

@login_manager.user_loader
def load_user(user):
    return User.get(user)

#Routing
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    user = {'username' : 'Hassan'}
    return render_template('index.html', user=user, css_link=url_for('static', filename='css/index.css')) 
    #url_for erlaubt website-spezifisches css und anwendung von html-vererbung zusammen

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_page = "login.html"
    if request.method == 'POST' and 'username_email' in request.form and 'password' in request.form:
        user = cur.get_user(request.form['username_email'], request.form['username_email'], request.form['password'])
        if  user != None:
            if request.form.getList('remember_me'):
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=5)
                #remembers session details (username, password, email, id) for 5 days
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect("/index.html", code=302)
        else:
            return render_template(login_page, type='error', title="Sign In - Error Occured", form=LoginForm())
    elif ('username' or 'email') in session:
        return render_template(login_page, type='logged_in', title="Sign In - Logged In", form=LoginForm())
    else:
        return render_template(login_page, title="Sign In", form=LoginForm())
        
            
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
def new_entry():
    abort(401)

@app.route('/entry/<int:entry_id>',  methods=['GET'])
def show_entry(entry_id):
    abort(401)
