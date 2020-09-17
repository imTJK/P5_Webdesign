from flask import Flask, render_template
from flask_login import LoginManager, current_user
from Webserver.config import Config
import sys

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)

from Webserver import routes