from flask import Flask, render_template
from Webserver.config import Config


app = Flask(__name__)
app.config.from_object(Config)

from Webserver import routes