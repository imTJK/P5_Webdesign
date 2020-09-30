class EmailBody(object):
    def __init__(self, recipient, link):
        self.recipient = recipient
        self.link = link

    def password_reset(self):
        text = '''
                <body>
                    <p>Hallo {},<br>
                    <br>
                    Du erh&auml;lst diese E-Mail weil du ein zur&uuml;cksetzen deines passwortes angefordert hast. <br>
                    Falls du dies nicht getan haben solltest ignoriere diese E-Mail einfach.<br>
                    <br>
                    Wenn du dein Passwort zur&uuml;cksetzen willst dann klicke bitte <a href={}> hier</a>.<br>
                    <hr>
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(self.recipient, self.link)
        return text
    
    def confirm_reset(self):
        text ='''
                <body>
                    <p> Hallo {},<br>
                    <br>
                    Dein Passwort wurde erfolgreich zur&uuml;ckgesetzt.<br>
                    Du kannst dich auch direkt <a href={}>hier</a> anmelden.<br>
                    <hr>
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(self.recipient, self.link)
        return text
    
    def activation(self):
        text = '''
                <body>
                    <p>Hallo {},<br>

                    bitte best&auml;tige deine E-mail addresse <a href={}>hier</a>.
                    <hr>
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(self.recipient, self.link)
        return text

    def entry_message(self, message, user_email, username,  entry_title):
        text = '''
            <body>
                <p>Hallo {},<br>

                {} hat eine Anfrage bezüglich deines <a href={}>Artikels \"{}\"</a> gestellt.
                <hr>
                <br>
                {}
                <br>
                {}
                <hr>
                Weiterer Kontakt ist zurzeit erst per gegenseitigem E-Mailen möglich. Wir bitten um Verständnis.
                <br>
                Mit freundlichen Gr&uuml;&szlig;en<br>
                dein Leihwas Team :)
                </p>
            </body>
        '''.format(self.recipient, username, self.link, entry_title, message, user_email)
        return text