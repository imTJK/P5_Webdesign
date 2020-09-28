import sys, os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import zlib

from Webserver import db

def NullColumn(*args,**kwargs):
    kwargs["nullable"] = kwargs.get("nullable",True)
    return db.Column(*args,**kwargs)


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(240))
    imgs_id = db.Column(db.Integer, db.ForeignKey('imgs.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, index=True, server_default=str(datetime.utcnow))

    def __repr__(self):
        return '<Entry title {}>'.format(self.title)
    
    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = description


class Images(db.Model):
    __tablename__ = 'imgs'
    id = db.Column(db.Integer, primary_key=True)
    img_1 = NullColumn(db.LargeBinary(length=2**24))
    img_2 = NullColumn(db.LargeBinary(length=2**24))
    img_3 = NullColumn(db.LargeBinary(length=2**24))
    img_4 = NullColumn(db.LargeBinary(length=2**24))
    filetypes_id = db.Column(db.Integer, db.ForeignKey('filetypes.id'))

    def get_images(self):
        return [self.img_1, self.img_2, self.img_3, self.img_4]
    
    def get_filetypes(self):
        return [ft for ft in Filetypes.query.filter_by(id = self.id).first().get_filetypes() if ft is not int]


class Filetypes(db.Model):
    __tablename__ = 'filetypes'
    id = db.Column(db.Integer, primary_key=True)
    ft_1 = db.Column(db.String(5))
    ft_2 = db.Column(db.String(5))
    ft_3 = db.Column(db.String(5))
    ft_4 = db.Column(db.String(5))

    def get_filetypes(self):
        return [self.ft_1, self.ft_2, self.ft_3, self.ft_4]


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=str(datetime.utcnow))
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    user_entries = db.relationship('Entry', backref='author', lazy='dynamic', foreign_keys=[Entry.id], primaryjoin='Entry.id == User.id')
    security_question = db.Column(db.Integer, nullable = False)
    hashed_security_answer = db.Column(db.String(255), nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_active(self):
        self.is_active = True
    
    def __repr__(self):
        return '<User {}>'.format(self.username)