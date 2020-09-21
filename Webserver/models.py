import sys, os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import zlib

from Webserver import db

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.LargeBinary(length=(2**32)-1))
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, index=True, server_default=str(datetime.utcnow))

    def __repr__(self):
        return '<Entry title {}>'.format(self.title)
    
    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = zlib.compress(description)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, index=True, server_default=str(datetime.utcnow))
    user_entries = db.relationship('Entry', backref='author', lazy='dynamic', foreign_keys=[Entry.id], primaryjoin='Entry.id == User.id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)