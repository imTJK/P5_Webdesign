import sys, os
sys.path.append(os.path.dirname(__file__))

### local imports ###
from Webserver import app, login_manager, db
from Webserver.forms import EditForm, EntryEditForm, EntryForm, LoginForm, PasswordForm, RecoveryForm, RegistrationForm, SearchForm, UserEditForm
from Webserver.mailserver import Email
from Webserver.models import Entry, Filetypes, Images, User
from Webserver.templates.email_body import EmailBody

### python imports ###
from PIL import Image, UnidentifiedImageError
from _datetime import timedelta
import io

### package imports ###
from flask import render_template, abort, url_for, request, session, redirect, current_app, copy_current_request_context
from flask_wtf import FlaskForm
from flask_login import current_user, login_required, login_user, logout_user
from flask.helpers import flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText

### non-url specific functions ###
def flash_errors(form):
    if form:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"%s - %s" %(
                    getattr(form, field).label.text,
                    error
                ))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


def search_for(form):
    return url_for('search_entry', search_term = form.term.data, amount = 20, site = 0)

### global-variables ###
mail = Email(
    port = 465,
    password = '+F%8TVppQ@R-.37tcs`t4N', # needs to definetly be read from file later on
    email = 'p5.leihwas@gmail.com'
)


### Flask Code-Start ###
@app.before_first_request
def setup():
    
    for img in session.get('imgs'):
        if img and os.path.exists(img):     
           os.remove(img)

    session['standard_css'] = url_for('static', filename='css/homepage.css')
    session['img_id'] = 0
    session['imgs'] = []

@app.before_request
def request_handling():
    #deletes all temporarily saved images for last page the user was on
    for img in session.get('imgs'):
        if img and os.path.exists(img):     
            os.remove(img)

    session['imgs'] = []
    session['img_id'] = 0

#login_manager to handle User-specific Requests
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) #int-cast due to flask_login passing ids as Strings

#login-required callback
@login_manager.unauthorized_handler
def unauthorized_user():
    flash('Sie müssen eingeloggt sein um diese Funktion zu verwenden')
    return redirect(url_for('login'))

### Routing ###
@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/test/<length>', methods=['GET', 'POST'])
def test(length):
    css_template = session['standard_css']

    return render_template('test.html', css_link=css_template)


@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():    
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    css_template = session['standard_css']
    return render_template('homepage.html', css_link=css_template, search_form=search_form) 
    #css_link css und anwendung von html-vererbung zusammen mit Jinja2 Variablen


@app.route('/terms-of-service', methods=['GET', 'POST'])
def tos():    
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    #Terms of Service / Allgemeine Geschäftsbedingungen
    #nicht unbedingt notwendig
    abort(401)

@app.route('/login', methods=['POST', 'GET'])
def login():    
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    css_template = session['standard_css'] 
    #still to be added:
        #a function against brute force attacks - possibly cookie that logs log in attempts and stops them after 5 tries and resets every 30mins or so
            #possibly a captcha/OAuth-Integration
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm(request.form)
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.email_username.data).first()
        ##workaround for being able to use both the username and email to login with
        if user == None:
            user = User.query.filter_by(email=form.email_username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Falsche Login-Daten')
                return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(days=10))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            #netloc checks wether the page has a different domain-name then the one of our application / if the url is relative
            return redirect(url_for('homepage'))
        return redirect(next_page)
    elif request.method == 'POST' and not form.validate_on_submit():
        flash_errors(form)

    return render_template('login.html', title='Login', form=form, css_link=css_template, search_form=search_form)
        

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()

    #deletes remaining temporarily stored images
    for img in session['imgs']:
        if os.path.exists(img):
            os.remove(img)
    
    return redirect(url_for('homepage'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    css_template = session['standard_css']
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    form = RegistrationForm(request.form)
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None and  User.query.filter_by(email=form.email.data).first() is None:
            user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()

            email_body = EmailBody(recipient=user.username, link="http://127.0.0.1:5000" + url_for('confirm_account', confirm_id=generate_password_hash(user.email))).activation()
            
            mail.send_mail(
                subject='Leihwas - Account-Aktivierung',
                recipient=user.email,
                body=email_body
            )
          

            flash('Erfolgreich Registriert <br> Ein Bestätigungs-Link wurde an ihre Email versand')
            return redirect(url_for('homepage'))
        elif User.query.filter_by(username=form.username.data).first():
                if User.query.filter_by(email=form.email.data).first() is not None:
                    flash('Nutzername und E-Mail werden bereits für einen account verwendet')
                    return redirect(url_for('register'))
                flash('Benutzername bereits vergeben')
                return redirect(url_for('register'))
        elif User.query.filter_by(email=form.email.data).first() is not None:
            if User.query.filter_by(username=form.username.data).first() is not None:
                flash('Nutzername und E-Mail werden bereits für einen account verwendet')
                return redirect(url_for('register'))
            flash('Ein Nutzer mit der E-Mail-Adresses ist bereits registriert')
            return redirect(url_for('register'))
            
    elif not form.validate_on_submit() and request.method == 'POST':
        flash_errors(form)
        return redirect(url_for('register'))
    
    return render_template('register.html', title='Registrieren', form=form, css_link=css_template, search_form=search_form)



@app.route('/user/confirm/<confirm_id>', methods=['GET', 'POST'])
def confirm_account(confirm_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    form = RecoveryForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(confirm_id, user.email):
            user.set_active()
            db.session.commit()
            flash('Account erfolgreich aktiviert')
            return redirect(url_for('homepage'))
        else:
            flash('Inkorrekte Eingabe')
            return redirect(url_for('confirm_account', confirm_id = confirm_id))
    
    return render_template('confirm_account.html', form=form, search_form=search_form)



@app.route('/recover', methods=['POST', 'GET'])
def recover():
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    css_template = session['standard_css']
    form = RecoveryForm()
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User.query.filter_by(username=form.email.data).first()
            if not user:
                flash('Kein User konnte unter diesen Namen/Email gefunden werden')
                return redirect(url_for('recover'))

        email_body = EmailBody(recipient=user.username, link="http://127.0.0.1:5000" + url_for('confirm_recovery', recovery_id=generate_password_hash(user.email))).password_reset()
        mail.send_mail(
            subject='Passwort-Wiederherstellung',
            recipient=user.email,
            body=email_body
        )
        
        session['recovery_email'] = mail.recipient
        return redirect(url_for('homepage'))
    else:
        return render_template('recover.html', title='Passwort wiederherstellen', css_link = css_template, form=form, search_form=search_form)


@app.route('/recover/<recovery_id>', methods=['POST', 'GET'])
def confirm_recovery(recovery_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))
    
    css_template = session['standard_css']
    if 'recovery_email' in session and check_password_hash(recovery_id,session['recovery_email']):
        email_form = RecoveryForm()
        flash_errors(email_form)

        if request.method == 'POST' and email_form.validate_on_submit() and check_password_hash(recovery_id, email_form.email.data):
            if User.query.filter_by(email = email_form.email.data).first():
                session['user_recovery_email'] = User.query.filter_by(email = email_form.email.data).first().email
                return redirect(url_for('set_password', recovery_id=recovery_id))

        return render_template('confirm_recovery.html', css_link = css_template, form=email_form, search_form=search_form)

    return redirect(url_for('homepage'))


@app.route('/recover/<recovery_id>/set_password', methods=['POST', 'GET'])
def set_password(recovery_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    css_template = session['standard_css']
    if 'user_recovery_email' not in session:
        redirect(url_for('login'))
    
    form = PasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email = session['user_recovery_email']).first()
        user.set_password(form.password.data)
        mail.send_mail(
            subject = 'Ihr Passwort wurde erfolgreich geändert',
            recipient = session['user_recovery_email'],
            body = EmailBody(User.query.filter_by(email=session['user_recovery_email']).username).confirm_reset()
        )
        session['user_recovery_email'] = None
        
        return redirect(url_for('login'))
    else:
        return render_template('set_password.html', form = form, css_link=css_template, search_form=search_form)


@app.route('/entry/new-Entry', methods=['POST', 'GET'])
@login_required
def new_entry():
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    form = EntryForm()
    if request.method == 'POST' and form.validate_on_submit():
        imgs = [form.img_1.data, form.img_2.data, form.img_3.data, form.img_4.data]
        imgs_id = db.session.query(Images).count() + 1
        files = []

        for i in range(len(imgs)):
            if imgs[i] is not None:
                if len(imgs[i].read()) < 16000000:
                    if allowed_file(imgs[i].filename):
                        files.append(imgs[i].filename.split('.')[len(imgs[i].filename.split('.')) - 1])
                        imgs[i].stream.seek(0)
                        imgs[i] = bytes(imgs[i].read())
                    else:
                        flash('Unerlaubtes Dateiformat .'+ imgs[i].filename.split('.')[len(imgs[i].filename.split('.')) - 1])
                        return redirect(url_for('new_entry'))
                else:
                    flash('Die Datei: ' + imgs[i].filename + ' ist zu groß. Max = 16MB')
                    return redirect(url_for('new_entry'))
            else:
                files.append('')
                imgs[i] = 0

        ### Database Operations for smooth Displaying of Entries ###
        filetypes = Filetypes(
            id = imgs_id, 
            ft_1 = files[0],
            ft_2 = files[1],
            ft_3 = files[2],
            ft_4 = files[3]
        )
        db.session.add(filetypes)

        imgs = Images(
            id = imgs_id,
            img_1=imgs[0],
            img_2=imgs[1],
            img_3=imgs[2],
            img_4=imgs[3],
            filetypes_id = imgs_id
        )
        db.session.add(imgs)
        db.session.commit()

        entry = Entry(
            title = form.title.data,
            description = form.description.data,
            created_by_id = current_user.id,
            imgs_id = imgs_id
        )

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('new_entry.html', form=form, search_form=search_form)


@app.route('/entry/search/<search_term>/<int:amount>/<int:site>', methods=['POST', 'GET'])
def search_entry(search_term, amount, site):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))
    
    entries_list = Entry.query.filter(Entry.title.contains(search_term)).all()
    
    entries = {1 if site == 0 else site*amount : {
                'id' : None,
                'title' : None,
                'description' : None,
                'imgs' : [None]
            }}
    imgs = []
    filetypes = []


    for i in range(site * amount, site * amount + amount):
        
        if i < len(entries_list) and entries_list[i]:
            for image in Images.query.filter_by(id = entries_list[i].imgs_id).all():
                for img in image.get_images():
                    imgs.append(img)
            for filetype in Filetypes.query.filter_by(id = entries_list[i].imgs_id).all():
                for ft in filetype.get_filetypes():
                    filetypes.append(ft)
                
            entries[i] =  {
                        'id' : entries_list[i].id,
                        'title' : entries_list[i].title,
                        'description' : str(entries_list[i].description, 'utf-8'),
                        'imgs' : zip([img for img in imgs], [ft for ft in filetypes])
                        }
            imgs = []
            filetypes = []
        else:
            break
    if not entries[1 if site == 0 else site * amount]['id']:
        return render_template('no_results.html', css_link = session['standard_css'], search_form = search_form)
    
    return render_template('search_entry.html', css_link = session['standard_css'], entries = entries, amount=amount, search_form=search_form)


@app.route('/entry/<int:entry_id>',  methods=['POST', 'GET'])
def show_entry(entry_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    entry = Entry.query.filter_by(id=entry_id).first()
    imgs = [img for img in Images.query.filter_by(id=entry.imgs_id).first().get_images()]
    if not Entry:
        abort(404)
    
    

    if current_user.is_authenticated and current_user.id == entry.created_by_id:
        form = EditForm()
        if request.method == 'POST' and form.validate_on_submit():
            return redirect(url_for('edit_entry', entry_id = entry_id, entry = entry))

        return render_template('show_entry.html', entry = entry, form = form, search_form = search_form, images = imgs)
    else:
        return render_template('show_entry.html', entry = entry, search_form = search_form, images = imgs)



@app.route('/entry/edit/<int:entry_id>', methods=['POST', 'GET'])
@login_required
def edit_entry(entry_id): 
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    entry = Entry.query.filter_by(id=entry_id).first()
    if current_user.is_authenticated() and current_user.id == entry.created_by_id:
        form = EntryEditForm(obj = entry)

        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            flash('Eintrag wurde erfolgreich bearbeitet')
            return redirect(url_for('show_entry', entry_id = entry_id))
        
        return render_template('edit_entry.html', entry = entry)
    return redirect(url_for('homepage'))


@app.route('/user/edit/<int:user_id>', methods=['POST', 'GET'])
@login_required
def edit_account(user_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    if current_user.id == user_id:
        user = User.query.filter_by(id=user_id)
        form = UserEditForm(obj=user)

        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return redirect(url_for())
        render_template('edit_account.html', form=form, search_form=search_form)

            
@app.route('/user/<int:user_id>')
@login_required
def view_account(user_id):
    search_form = SearchForm()
    if request.method == 'POST' and search_form.validate_on_submit():
        return redirect(search_for(search_form))

    if 'user' in session and session['user'].id == user_id:
        edit_form = EditForm()
        user = User.query.filter_by(id=user_id)

        if request.method == 'POST' and edit_form.validate_on_submit():
            return redirect(url_for('edit_account'), user_id=user_id)
        return render_template('account.html', user = user, search_form=search_form)
    
    flash('Inkorrekte User-ID')
    return redirect(url_for('homepage'))


@app.route('/image/<int:entry_id>/<int:image_id>', methods=['GET'])
def show_image(entry_id, image_id):
    with app.test_request_context():
        images = Images.query.filter_by(id = entry_id).first()
        img = images.get_images()[image_id]
        filetype = 'JPEG' if images.get_filetypes()[image_id] == "jpg" else images.get_filetypes()[image_id].upper()
        
        img_id = 0 if session.get('img_id') is None else session.get('img_id')
        img_path = '{}\\{}.{}'.format(app.config['UPLOAD_FOLDER'], img_id, filetype.lower())
        try:
            img = Image.open(io.BytesIO(img))
            img.save(img_path, filetype)
        except UnidentifiedImageError as e:
            print(e)
        
        #deletion-handling
        session['img_id'] = img_id + 1
        session['imgs'] = [img_path] if session.get('imgs') is None else session.get('imgs').append(img_path)
        return send_from_directory(app.config['UPLOAD_FOLDER'], '{}.{}'.format(img_id, filetype.lower()))