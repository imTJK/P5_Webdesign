import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#HTTP Error 403: Forbidden
#Wird später gefixt
class Email(object):
    def __init__(self, email_sender, email_recipients, subject, html_message):
        self.message = Mail(
            from_email=email_sender,
            to_emails=email_recipients,
            subject=subject,
            html_content=html_message)

       
    def send_mail(self):
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(self.message)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    mail = Email("from_email@example.com", "to@example.com", "First E-Mail-Test with Twilio SendGrid", '<strong> Now this is podracing </strong>')
    mail.send_mail()