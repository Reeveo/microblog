from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

    '''
    Table for Users, ID is the primary key and is linked to the posts table as a foreign key (Post.User_id) 
    Parameters, state integer or string, db.String is variable length and not fixed
    http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/table_config.html
    Usermixin implements the generic implementations - is_authenticated, is_active, is_anonymous, get_id()
    '''
    #Set up the User table
class User(Usermixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

        # This repr allows you to use flask shell to print the username - also used below for posts
    def __repr__(self):
        return '<User {}>'.format(self.username)

        #Function to generate a hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

        #Function to check if the password is correct, boolean where true is returned if it is correct.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
        # Obtain a avatar picture from Gravatar (wordpress company). This needs the email to be in lower case to work
        # d = deault icon to use
        #s = size e.g. 80 == 80 pixels
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)
    
    
    
    # Datetime is used to timestampe when the post is created which allows for filtering etc. UTC specifically to avoid time conflicts
    #Set up the Post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

       # This is used tin the python shell to print posts
    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user.loader
def load_user(id):
    return User.query.get(int(id))
