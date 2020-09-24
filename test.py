import sys, os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import random
import re
from PIL import Image
from flask import current_app

from Webserver import app
from werkzeug.security import generate_password_hash, check_password_hash
from Webserver.models import Entry, Images, User
from Webserver import db
from Webserver.mailserver import Email
import io

def random_string(length):
    s = ''
    for x in range (0,length):
        abc = list('abcdefghijklmnopqrstuvwxyz')
        s += abc[random.randint(0, len(abc) - 1)]
    return s

def bin_to_img(bin):
    img = Image.open(io.BytesIO(bin))
    img.show()


