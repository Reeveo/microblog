from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=5,message="This needs to be at least 2 characters long")])
	password = PasswordField("Password", validators=[DataRequired(), Length(5,message="It has got to be longer than that!")])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Sign in")


