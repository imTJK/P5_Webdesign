import sys, os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import random
import re
from flask import current_app

from Webserver import app
from Webserver.cursor import Cursor
from werkzeug.security import generate_password_hash, check_password_hash
from Webserver.models import User, Entry
from Webserver import db
from Webserver.mailserver import Email

def random_string(length):
    s = ''
    for x in range (0,length):
        abc = list('abcdefghijklmnopqrstuvwxyz')
        s += abc[random.randint(0, len(abc) - 1)]
    return s

mail = Email(465, "+F%8TVppQ@R-.37tcs`t4N", "p5.leihwas@gmail.com")
mail.send_mail('tjorvenkoopmann2001@gmail.com', 'Hurensoh')