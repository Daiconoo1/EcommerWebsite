import email_validator
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DecimalField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from .models import CustomerRegister 

 

class CustomrerSignupForm(FlaskForm):
	name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=100), 
		Regexp('^[A-Za-z" "]*$', 0, 'Name must be only alphabeth ')])
	
	email =  StringField('Email:', validators=[DataRequired(), Email()])
	address = TextAreaField('Address:', validators=[DataRequired(), 
		Regexp('^[A-Za-z0-9" "]*$', 0, 'Address can only have combination of either alphabeth or number')])
	username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=20),
		Regexp('^[A-Za-z0-9]*$', 0, 'Usernames must have combination of either alphabeth or number')])
	password = PasswordField ('Password:', validators=[DataRequired()])
	confirm_password = PasswordField ('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
	mobile = StringField('Mobile:', validators=[DataRequired(),Length(min=10, max=10), Regexp('^[0-9]*$', 0,'Mobile must have only numbers')])
	submit = SubmitField('SignUp')

	def validate_email(self,email):
		customer =CustomerRegister.query.filter_by(email=email.data).first()
		if customer:
			raise ValidationError ('This email has been taken')

	def validate_username(self,username):
		customer =CustomerRegister.query.filter_by(username=username.data).first()
		if customer:
			raise ValidationError ('This username has been used by another customer')

	 

class CustomerLoginForm(FlaskForm):
	email =  StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField ('Password:', validators=[DataRequired()])
	submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
	password = PasswordField ('Password:', validators=[DataRequired()])
	confirm_password = PasswordField ('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

class RequestForm(FlaskForm):
	email =  StringField('Email:', validators=[DataRequired(), Email()])
	submit = SubmitField('Request')

	def validate_email(self,email):
		user =CustomerRegister.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError ('You have to sign up first', 'danger')
 

