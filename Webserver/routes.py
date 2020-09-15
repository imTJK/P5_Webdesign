from flask import render_template, abort, url_for, request
from Webserver import app

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    user = {'username' : 'Hassan'}
    return render_template('index.html', user=user, css_link=url_for('static', filename='css/index.css')) 
    #url_for erlaubt website-spezifisches css und anwendung von html-vererbung zusammen

@app.route('/login', methods=['POST', 'GET'])
def login():
    abort(401)

@app.route('/register', methods=['POST', 'GET'])
def register():
    abort(401)

@app.route('/entry/new-Entry', methods=['POST', 'GET'])
def new_entry():
    abort(401)

@app.route('/entry/<int:entry_id>',  methods=['GET'])
def show_entry(entry_id):
    abort(401)
