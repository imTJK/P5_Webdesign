from flask import render_template
from Webserver import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Hassan'}
    return render_template('index.html', user=user)

@app.route('/item/<int:item_id>')
def items(item_id):
    return 'This is the ' + str(item_id) + ' Item'
