import sys, os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import random
import re
from PIL import Image
from flask import current_app

from Webserver import app
from werkzeug.security import generate_password_hash, check_password_hash
from Webserver.models import Entry, Filetypes, Images, User
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


for i in range(20, 120):
    filetypes = Filetypes(
        id = i,
        ft_1 = 'jpg' 
    )
    db.session.add(filetypes)
    db.session.commit()
    images = Images(
        id = i, 
        filetypes_id = i,
        img_1 = bytes(open(r"C:\Users\Tjorven\Desktop\Programmieren\P5\P5_Webdesign\Webserver\static\res\_tmp\0.jpeg", 'rb').read())
    )
    db.session.add(images)
    db.session.commit()
    entry = Entry(
        id = i,
        title = random_string(10),
        description = random_string(100),
        imgs_id = i,
        created_by_id = 1
    )
    
    
    db.session.add(entry)

db.session.commit()