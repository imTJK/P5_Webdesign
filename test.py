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
        abc = list('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789')
        s += abc[random.randint(0, len(abc) - 1)]
    return s

def bin_to_img(bin):
    img = Image.open(io.BytesIO(bin))
    img.show()

def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


spice_list=['anis', 'chili', 'kreuzkümmel', 'gewürznelken', 'ingwer', 'kardamom', 'kurkuma', 'muskat', 'paprika', 'pfeffer', 'piment', 'safran', 'vanille', 'wacholderbeere', 'zimt']
files = []
imgs = [r'img1.jpg', r'img2.jpg', r'img3.jpg', r'img4.jpg', r'img5.jpg', r'img6.jpg']

for i in range(len(imgs)):
    if imgs[i] is not None:
        imgs[i] = Image.open(imgs[i])
        files.append(imgs[i].filename.split('.')[len(imgs[i].filename.split('.')) - 1])
        imgs[i] = image_to_byte_array(imgs[i])


for i in range(1, 101):
    spice = spice_list[random.randint(0, len(spice_list) - 1)]
    imgs_id = i
 
    
    filetypes = Filetypes(
        id = imgs_id,
        ft_1 = 'jpg',
        ft_2 = 'jpg',
        ft_3 = 'jpg'
    )
    db.session.add(filetypes)
    db.session.commit()

    images = Images(
        id = imgs_id,
        filetypes_id = imgs_id,
        img_1 = imgs[random.randint(0, len(imgs) - 1)],
        img_2 = imgs[random.randint(0, len(imgs) - 1)],
        img_3 = imgs[random.randint(0, len(imgs) - 1)]
    )
    db.session.add(images)
    db.session.commit()

    entry = Entry(
        id = imgs_id,
        title = spice + '-Falafel',
        description = 'Diese Falafel ist außen wunderbar kross gebraten und innen lecker saftig. \n Mit {} gewürzt.'.format(spice),
        created_by_id = random.randint(1, 3),
        imgs_id = images.id
    )
    db.session.add(entry)
    db.session.commit()