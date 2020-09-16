from flask import Flask, render_template
from flask_login import LoginManager
import mariadb
from Webserver.config import Config
import sys

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

try:
    conn = mariadb.connect(
        user = "root",
        password = "",
        host = "localhost",
        port = 3306)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

from Webserver import routes