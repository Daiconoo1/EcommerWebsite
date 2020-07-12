import email_validator
from flask_wtf import FlaskForm 
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DecimalField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from .models import AdminUser 


class RegisterAdmint(FlaskForm):
	name = StringField('Name:', validators=[DataRequired(), Length(min=2, max=100),
	Regexp('^[A-Za-z" "]*$', 0, 'Name must be only alphabeth ') ])	
	adminemail =  StringField('Email:', validators=[DataRequired(), Email()])	 
	username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=20),
		Regexp('^[A-Za-z0-9]*$', 0, 'Usernames must have combination of either alphabeth or number')])
	password = PasswordField ('Password:', validators=[DataRequired()])
	confirm_password = PasswordField ('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
	mobile = StringField('Mobile:', validators=[DataRequired(),Length(min=10, max=10), Regexp('^[0-9]*$', 0,'Mobile must have only numbers')])
	submit = SubmitField('Register')


	def validate_email(self,email):
		admin =AdminUser.query.filter_by(email=email.data).first()
		if admin:
			raise ValidationError ('This email has been taken')

	def validate_username(self,username):
		admin =AdminUser.query.filter_by(username=username.data).first()
		if admin:
			raise ValidationError ('This username has been used by another admin')
 	
class AdminLoginForm(FlaskForm):
 	adminemail =  StringField('Email:', validators=[DataRequired(), Email()])
 	password = PasswordField ('Password:', validators=[DataRequired()])
	 	

 

