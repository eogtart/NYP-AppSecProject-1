from datetime import timedelta
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_paranoid import Paranoid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_recaptcha import ReCaptcha
from os import path, urandom
import logging

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # if database.db does not exist in this path it creates a database
        db.create_all(app=app)
        print('Created Database! ')


# Some logging I guess
logging.getLogger("werkzeug").setLevel('WARNING')
logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcAbWchAAAAAMbS7JaIydkj2vWeXLGCzA8V27gR'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcAbWchAAAAACbre01_DW8CbZnP41SmCTS_u2jM'
recaptcha = ReCaptcha(app)

# csrf protection, Use only when HTTPS Enabled
csrf = CSRFProtect(app)
csrf.init_app(app)

# User is marked as logged out automatically when existing session suddenly gets hijacked.
# Prevents Session Hijacking.
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

DB_NAME = 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SECRET_KEY']= '5468576D597133743677397A24432646294A404E635266556A586E3272347537'

# Session Timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Set stronger cookie.
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


#Rate limiting, limiting the requests sent from client
limiter = Limiter(app, key_func=get_remote_address,  default_limits=["500 per day"])
limiter.init_app(app)

db = SQLAlchemy(app)

# enables the database
create_database(app)
bcrypt = Bcrypt(app)
# hashes the passwords 'utf-8' is used check 'models.py'

def admin_user():
    from website.models import User
    db.create_all()
    with app.app_context():
        admin = User(admin=1, username='admin', password='admin123',email_address='swissoffical@gmail.com', gender='rather not say', twofa="Enabled")
        #query.filter_by avoids coding in raw sql, making sql injection impossible for the attacker
        if not User.query.filter_by(admin = admin.id).first() and not User.query.filter_by(email_address = admin.email_address).first() and not User.query.filter_by(username = admin.username).first():
            db.session.add(admin)
            db.session.commit()

login_manager = LoginManager(app)
login_manager.login_view = 'landing_page'
login_manager.login_message_category = 'info'
# makes the message flashed blue when user is not authorised/logged in.

from website import routes
