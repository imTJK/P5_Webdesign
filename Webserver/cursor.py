
### Probably completly useless due to switch to SQLAlchemy for easier security-Integration ###

import sys, os
sys.path.append(os.path.dirname(__file__))

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
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        self.cur = self.conn.cursor()
        self.cur.execute('USE p5_database')

    

    def get_user(self, username, email, password):
        #SQL-Code by Tjorven
        #Works, returns dict with id, username and email for use in html-templates)
        user = {'id' : None,
                'username' : None,
                'email' : None}
                
        #enabling login with only e-mail or username
        if username == None:
            username = ""
        elif email == None:
            email = ""
        
        self.cur.execute('SELECT 1, password FROM p5_database.users WHERE username=? OR email=?', (username, email,))
        for x in self.cur:
            if (x[0] == 1 and check_password_hash(x[1], password)):
                self.cur.execute('SELECT id, username, email FROM p5_database.users WHERE(username=? OR email=? AND password=?)', (username, email, password))
                for(id, uname, mail) in self.cur:
                    user['id'] = id
                    user['username'] = uname
                    user['email'] = mail
                return user
            else:
                return None
    


    def add_user(self, username, email, password):
        #SQL-Code by Tjorven
        #Responses:
            #0: User created successfully 
            #1: Username already taken
            #2: E-Mail already in use
        self.cur.execute('SELECT EXISTS(SELECT 1 FROM p5_database WHERE username=?', (username))
        for user in self.cur:
            if user[0] == 0:
                self.cur.execute('SELECT EXISTS(SELECT 1 FROM p5_database WHERE email=?', (email))
                for mail in self.cur:
                    if(mail[0] == 0):
                        self.cur.execute('INSERT INTO p5_database.users(username, password, email) VALUES(?, ?, ?)', (username, email, generate_password_hash(password)))
                        return 0
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

    def get_user_entries(self, user_id):
        #only called when logged in, therefore no authentication or checking if the user exists
        entries =  []
        entry = {
            'id' : None,
            'created_time' : None,
            'is_private' : None
        }
        
        self.cur.execute('SELECT id, created_time, is_private FROM p5_database.entries WHERE created_by=?', (user_id))
        for e in self.cur:
            entry['id'] = e[0]
            entry['created_time'] = e[1]
            entry['is_private'] = e[2]
            entries.append(e)

        return entries

    def close_connection(self):
        if self.conn != None:
            self.conn.close()