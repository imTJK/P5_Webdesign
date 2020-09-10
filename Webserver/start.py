from flask import Flask, request, url_for, redirect, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testLink')
def test_link():
    name = "Hassan"
    return render_template('testLink.html', **locals())

@app.route('/test.php')
def php():
    render_template('')

if __name__ == '__main__':
    app.run()