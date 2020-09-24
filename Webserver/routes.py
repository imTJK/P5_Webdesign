import sys, os
sys.path.append(os.path.dirname(__file__))

### local imports
from Webserver import app, login_manager, db
from Webserver.forms import EntryForm, EntryImagesForm, LoginForm, PasswordForm, RecoveryForm, RegistrationForm, SearchForm
from Webserver.mailserver import Email
from Webserver.models import Entry, Images, User
from Webserver.templates.email_body import EmailBody

### package imports
from flask import render_template, abort, url_for, request, session, redirect, current_app
from flask_wtf import FlaskForm
from flask_login import current_user, login_required, login_user, logout_user
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from _datetime import timedelta
from email.mime.text import MIMEText
from PIL import Image
import io
import zlib


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

#search_form = SearchForm()

mail = Email(
    port = 465,
    password = '+F%8TVppQ@R-.37tcs`t4N', # needs to definetly be read from file later on
    email = 'p5.leihwas@gmail.com'
)

### Flask Code-Start ###

@app.before_first_request
def setup():
    session['standard_css'] = url_for('static', filename='css/homepage.css')

#login_manager to handle User-specific Requests
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) #int-cast due to flask_login passing ids as Strings

#login-required callback
@login_manager.unauthorized_handler
def unauthorized_user():
    return redirect(url_for('login'))

###   Routing   ###
@app.route('/test/<length>', methods=['GET', 'POST'])
def test(length):
    css_template = session['standard_css']
    entries_list = Entry.query.limit(length).all()

    entries = {0 : {
                'id' : None,
                'title' : None,
                'description' : None,
                'imgs' : [None]}}
    imgs = []

    for i in range(len(entries_list)):
        for image in Images.query.filter_by(id = entries_list[i].imgs_id):
            for img in image.get_images():
                imgs.append(zlib.compress(img))
        

        entries[i] =  {
                    'id' : entries_list[i].id,
                    'title' : entries_list[i].title,
                    'description' : str(entries_list[i].description, 'utf-8'),
                    'imgs' : imgs
                    }
        imgs = []

    #nested dict for getting entries and images in one place, best for showing in large list and easy to 

    return render_template('test.html', css_link=css_template, entries=entries)


@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET'])
def homepage():
    css_template = session['standard_css']
    return render_template('homepage.html', css_link=css_template) 
    #css_link css und anwendung von html-vererbung zusammen mit Jinja2 Variablen



@app.route('/terms-of-service', methods=['GET'])
def tos():
    #Terms of Service / Allgemeine Geschäftsbedingungen
    #nicht unbedingt notwendig
    pass



@app.route('/register', methods=['POST', 'GET'])
def register():
    css_template = session['standard_css']
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = RegistrationForm(request.form)
    flash_errors(form)
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None and  User.query.filter_by(email=form.email.data).first() is None:
            user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
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
            
    elif not form.validate_on_submit():
        flash_errors(form)
        return render_template('register.html', title='Registrieren', form=form, css_link=css_template)
    
    return render_template('register.html', title='Registrieren', form=form, css_link=css_template)



@app.route('/login', methods=['POST', 'GET'])
def login():
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

    return render_template('login.html', title='Login', form=form, css_link=css_template)
        


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('homepage'))



@app.route('/recover', methods=['POST', 'GET'])
def recover():
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
        return render_template('recover.html', title='Passwort wiederherstellen', css_link = css_template, form=form)



@app.route('/recover/<recovery_id>', methods=['POST', 'GET'])
def confirm_recovery(recovery_id):
    css_template = session['standard_css']
    if 'recovery_email' in session and check_password_hash(recovery_id,session['recovery_email']):
        email_form = RecoveryForm()
        flash_errors(email_form)

        if request.method == 'POST' and email_form.validate_on_submit() and check_password_hash(recovery_id, email_form.email.data):
            if User.query.filter_by(email = email_form.email.data).first():
                session['user_recovery_email'] = User.query.filter_by(email = email_form.email.data).first().email
                return redirect(url_for('set_password', recovery_id=recovery_id))

        return render_template('confirm_recovery.html', css_link = css_template, form=email_form)

    return redirect(url_for('homepage'))



@app.route('/recover/<recovery_id>/set_password', methods=['POST', 'GET'])
def set_password(recovery_id):
    css_template = session['standard_css']
    if 'user_recovery_email' not in session:
        redirect(url_for('login'))
    
    form = PasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email = session['user_recovery_email']).first()
        user.set_password(form.password.data)
        mail.send_mail(
            subject = 'Passwort wurde geändert',
            recipient = session['user_recovery_email'],
            body = EmailBody(User.query.filter_by(email=session['user_recovery_email']).username).confirm_reset()
        )
        session['user_recovery_email'] = None
        
        return redirect(url_for('login'))
    else:
        return render_template('set_password.html', form = form, css_link=css_template)



@app.route('/entry/new-Entry', methods=['POST', 'GET'])
@login_required
def new_entry():
    form = EntryForm()
    if request.method == 'POST' and form.validate_on_submit():
        imgs = [form.img_1.data, form.img_2.data, form.img_3.data, form.img_4.data]
        

        for i in range(len(imgs)):
            print(imgs[i])
            if imgs[i] is not None:
                if len(imgs[i].read()) < 16000000:
                    if allowed_file(imgs[i].filename):
                        imgs[i] = imgs[i].read()
                    else:
                        flash('Unerlaubtes Dateiformat .'+ imgs[i].filename.split('.')[len(imgs[i].filename.split('.')) - 1])
                        return redirect(url_for('new_entry'))
                else:
                    flash('Die Datei: ' + imgs[i].filename + ' ist zu groß. Max = 16MB')
                    return redirect(url_for('new_entry'))
            else:   
                imgs[i] = 0

        imgs_id = db.session.query(Images).count() + 1

        imgs = Images(
            id = imgs_id,
            img_1=imgs[0],
            img_2=imgs[1],
            img_3=imgs[2],
            img_4=imgs[3]
        )

        entry = Entry(
            title = form.title.data,
            description = form.description.data,
            created_by_id = current_user.id,
            imgs_id = imgs_id
        )

        db.session.add(imgs)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('new_entry.html', form=form)



@app.route('/entry/search/<search_term>', methods=['POST', 'GET'])
def search_entry(search_term):

    if request.method == 'POST':
        pass #search function
    
    
    
    entries = Entry.query.filter(Entry.title.contains(search_term))
    render_template('search_entry.html', entries = entries)


@app.route('/entry/<int:entry_id>',  methods=['POST', 'GET'])
def show_entry(entry_id):
    abort(401)


@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def account_page(user_id):
    if 'user' in session and session['user'].id == user_id:
        return render_template('account.html')

@app.route('/image/<image_id>', methods=['GET'])
def show_image(image_id):
    id_dc = zlib.decompress(image_id)
    img = Image.open(io.BytesIO(id_dc))
    return img