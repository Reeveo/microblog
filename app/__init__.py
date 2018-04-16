from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
# Initialise the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialises the flask login 
login = LoginManager(app)

# this is needed to prevent access to pages if not logged in. It tells Flask-Login what the view function is which handles logins (url_for page)
login.login_view = 'login'

from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)
