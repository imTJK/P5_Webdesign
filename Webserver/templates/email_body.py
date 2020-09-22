class EmailBody(object):
    def __init__(self, type, recipient, link):
        if type == 'password_reset':
            self.text = '''
                <body>
                    <p>Hallo {},<br>
                    <br>
                    Du erh&auml;lst diese E-Mail weil du ein zur&uuml;cksetzen deines passwortes angefordert hast. <br>
                    Falls du dies nicht getan haben solltest Ignoriere bitte diese E-mail.<br>
                    <br>
                    Wenn du dein Passwort zur&uuml;cksetzen willst dann klicke bitte <a href={}> hier</a>.<br>
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(recipient, link)

        elif type == 'password_reset_confirmation':
            self.text ='''
                <body>
                    <p> Hallo {},<br>
                    <br>
                    Dein Passwort wurde erfolgreich zur&uuml;ckgesetzt.<br>
                    Du kannst dich auch direkt <a href={}>hier</a> anmelden.<br>
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(recipient, link)

        elif type == 'activation':
            self.text = '''
                <body>
                    <p>Hallo {},<br>

                    bitte best&auml;tige deine E-mail addresse <a href={}>hier</a>.
                    <br>
                    Mit freundlichen Gr&uuml;&szlig;en<br>
                    dein Leihwas Team :)
                    </p>
                </body>
            '''.format(recipient, link)
        else:
            print("Incorrect Type for Email-Class")