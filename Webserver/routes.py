from flask import render_template, abort, url_for, request, session
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
    cur = Cursor('mariadbtest', 'password', 'localhost', 3306)

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
                #remembers session details (username, password, email, id) for 5 days
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=5)
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
        else:
            return render_template(login_page, type='error')
    elif ['username'] or ['email'] in session:
        return render_template(login_page, type='logged_in')
    else:
        return render_template(login_page)
        
            
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        pass
    abort(401)

@app.route('/entry/new-Entry', methods=['POST', 'GET'])
def new_entry():
    abort(401)

@app.route('/entry/<int:entry_id>',  methods=['GET'])
def show_entry(entry_id):
    abort(401)
