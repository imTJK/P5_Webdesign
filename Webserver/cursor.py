import sys
import mariadb
from werkzeug.security import generate_password_hash, check_password_hash

class Cursor(object):
    conn = None
    cur = None
    def __init__(self, user, password, host, port, db):
        try:
            self.conn = mariadb.connect(
                user = user,
                password = password,
                host = host,
                port = port,
                database = db)
            self.cur = self.conn.cursor()
            self.cur.execute('USE p5_database')
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    

    def get_user(self, username, email, password):
        #SQL-Code by Adrian (WIP)
        user = {'id' : None,
                'username' : None,
                'email' : None}
        if(self.cur.execute('SELECT 1 FROM p5_database.user WHERE(username=? OR email=?)', (username, email)) == 1):
            #and check_password_hash(self.cur.execute('SELECT password FROM p5_database.user WHERE(username=? OR email=?)', (username, email)), password)):
            self.cur.execute('SELECT id, username, email FROM p5_database.user WHERE(username=? OR email=? AND password=?)', (username, email, password))

            for(id, uname, mail) in self.cur:
                user['id'] = id
                user['username'] = uname
                user['email'] = mail
            return user
        else:
            return None

    def add_user(self, username, email, password):
        #SQL-Code by Adrian (WIP)
        #Reasons: 
            #1: Username already taken
            #2: E-Mail already in use
        if(self.cur.execute('SELECT EXISTS(SELECT 1 FROM p5_database WHERE username=?', (username)) == 0):
            if(self.cur.execute('SELECT EXISTS(SELECT 1 FROM p5_database WHERE email=?', (email)) == 0):
                self.cur.execute('INSERT INTO p5_database.user(username, password, email) VALUES(?, ?, ?)', (username, email, generate_password_hash(password)))
            else:
                return 1
        else:
            return 2

    def add_entry(self):
        #SQL-Code by Adrian (WIP)
        pass
    
    def get_entry(self):
        #SQL-Code by Adrian (WIP)
        pass