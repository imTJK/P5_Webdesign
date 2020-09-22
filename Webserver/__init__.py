import sys, os
sys.path.append(os.path.dirname(__file__))

from Webserver.config import Config

from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config(
    user = 'root',
    password = '',
    domain = 'localhost',
    database = 'p5_database'
))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

Bootstrap(app)

from Webserver import routes, models