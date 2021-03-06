from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)




'''
Table for Users, ID is the primary key and is linked to the posts table as a foreign key (Post.User_id) 
Parameters, state integer or string, db.String is variable length and not fixed
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/table_config.html
Usermixin implements the generic implementations - is_authenticated, is_active, is_anonymous, get_id()
'''
   
    #Set up the User table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        "User", secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref("followers", lazy="dynamic"), lazy="dynamic")

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
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
        
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

        
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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
