import sys, os
sys.path.append(os.path.dirname(__file__))

class Config(object):
    def __init__(self, user, password, domain, database):
        self.SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_key_is_secret'
        self.MAIL_SERVER = 'tjorvenkoopmann2001@gmail.com'
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{domain}/{database}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg', 'nef', 'cr2']
        self.UPLOAD_FOLDER = r'C:\Users\Tjorven\Desktop\Programmieren\P5\P5_Webdesign\Webserver\static\res\_tmp'
        self.SECURITY_QUESTIONS =  [(0, 'Wie hieß dein erstes Haustier?'),(1, 'Straße, in der Sie als Kind gewohnt haben?'), (2, 'Bester Freund in Ihrer Kindheit?'), (3, 'Vorname Ihres Großvaters?')]
        