import sys, os
sys.path.append(os.path.dirname(__file__))

import smtplib, ssl

class Email(object):
    def __init__(self, port, password, email):
        self.email, self.password = email, password
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            self.server = server


    def send_mail(self, recipient, body):
        self.server.connect('smtp.gmail.com')
        self.server.login(self.email, self.password)
        self.server.sendmail(self.email, recipient, body)