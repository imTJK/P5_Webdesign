from cursor import Cursor
import re
from werkzeug.security import generate_password_hash, check_password_hash

cu = Cursor('root', '', 'localhost', 3306, "p5_database")

cu.cur.execute('SELECT password FROM user WHERE username=?',('Hassan',))
for x in cu.cur:
    #cu.cur returns values as arrays, hence the x[0]
    p_hash = x[0]

user = cu.get_user("Hassan", "Hassan@mail.com", "HassansPwd")
if user != None:
    for key in user:
        print(str(key) + ": " + str(user[key]))
