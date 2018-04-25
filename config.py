import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    #Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Session cookie settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    REMEMBER_COOKIE_DURATION = timedelta(days=1)
    
    # Email settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME =os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["admin@test.com"]

    #Post settings
    POSTS_PER_PAGE= 25
