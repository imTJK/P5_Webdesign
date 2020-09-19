import sys, os
sys.path.append(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_key_is_secret'
    MAIL_SERVER = 'tjorvenkoopmann2001@gmail.com'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/p5_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False