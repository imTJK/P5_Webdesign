from flask import render_template, abort, url_for, request
from Webserver import app, login_manager, conn
from Webserver.forms import LoginForm

#Routing
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    user = {'username' : 'Hassan'}
    return render_template('index.html', user=user, css_link=url_for('static', filename='css/index.css')) 
    #url_for erlaubt website-spezifisches css und anwendung von html-vererbung zusammen

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_manager(user)

@app.route('/register', methods=['POST', 'GET'])
def register():
    abort(401)

@app.route('/entry/new-Entry', methods=['POST', 'GET'])
def new_entry():
    abort(401)

@app.route('/entry/<int:entry_id>',  methods=['GET'])
def show_entry(entry_id):
    abort(401)
