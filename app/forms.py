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
	
	'''
	When you add any methods that match the pattern validate_<field_name>, 
	WTForms takes those as custom validators and invokes them in addition to the stock validators.
	The below validators check to see if the username or email is present in the database,
	if it is then it will return a ValidationError.
	'''
	
	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError("Please use a different username")
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError("Please use a different email address")
			
