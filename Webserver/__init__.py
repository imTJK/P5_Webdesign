from flask import Flask, render_template
from flask_login import LoginManager
from Webserver.config import Config


app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)


from Webserver import routes