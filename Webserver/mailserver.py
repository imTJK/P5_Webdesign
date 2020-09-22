import sys, os
sys.path.append(os.path.dirname(__file__))

import smtplib, ssl
from email.mime.text import MIMEText

class Email(object):
    def __init__(self, port, password, email):
        self.mail_adress, self.password, self.port = email, password, port
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            self.server = server


    def send_mail(self, subject, recipient, body):
        msg = MIMEText(body, 'html')
        msg['From'] = self.mail_adress
        self.recipient, msg['To'] = recipient, recipient
        msg['Subject'] = subject

        self.server.connect('smtp.gmail.com', self.port)
        self.server.login(self.mail_adress, self.password)
        self.server.sendmail(self.mail_adress, recipient, msg.as_string())
        self.server.quit()