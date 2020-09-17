from cursor import Cursor
from werkzeug.security import generate_password_hash

cur = Cursor('mariadbtest', 'password', 'localhost', 3306, "p5_database")
sel = cur.cur.execute('SELECT * FROM user')
print(sel)

user = cur.get_user("Hassan", "Hassan@mail.com", "HassansPwd")


if user != None:
    for x in user:
        print(x)