from cursor import Cursor
from werkzeug.security import generate_password_hash


print(generate_password_hash('HassansPwd'))

cur = Cursor('pma', '', 'localhost', 3306, "p5_database")
sel = cur.cur.execute('SELECT * FROM p5_database.users')
print(sel)



user = cur.get_user("Hassan", "Hassan@mail.com", "HassansPwd")


if user != None:
    for x in user:
        print(x)