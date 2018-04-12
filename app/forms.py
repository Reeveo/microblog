from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, NumberRange

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired("You need to enter you name"), NumberRange("2","Your full name...")])
	email = StringField("Email", validators=[DataRequired("You need to enter something here"), Email("This filed required a valid email address.")])
	nickname = StringField("What would you prefer to be called?", validators=[])
	password = PasswordField("Password", validators=[DataRequired(), NumberRange("5","Its got to be longer than that!")])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Sign in")