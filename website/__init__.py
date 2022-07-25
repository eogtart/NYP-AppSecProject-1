from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_paranoid import Paranoid
from os import path, urandom


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # if database.db does not exist in this path it creates a database
        db.create_all(app=app)
        print('Created Database! ')


app = Flask(__name__)

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

db = SQLAlchemy(app)

# enables the database
create_database(app)
bcrypt = Bcrypt(app)
# hashes the passwords 'utf-8' is used check 'models.py'
def admin_user():
    from website.models import User
    db.create_all()
    with app.app_context():
        admin = User(admin=1, username='admin', password='admin123',email_address='admin@example.com', gender='rather not say', twofa="Disabled")
        if not User.query.filter_by(admin = admin.id).first() and not User.query.filter_by(email_address = admin.email_address).first() and not User.query.filter_by(username = admin.username).first():
            db.session.add(admin)
            db.session.commit()

login_manager = LoginManager(app)
login_manager.login_view = 'landing_page'
login_manager.login_message_category = 'info'
# makes the message flashed blue when user is not authorised/logged in.


from website import routes
