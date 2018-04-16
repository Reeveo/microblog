from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from app.models import User

	
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=5,message="This needs to be at least 5 characters long")])
	password = PasswordField("Password", validators=[DataRequired(), Length(5,message="It has got to be longer than that!")])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Sign in")

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=5,message="This needs to be at least 5 characters long")])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Register")
	
	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError("Please use a different username")
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError("Please use a different email address")
			
