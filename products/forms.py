from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField, IntegerField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Regexp, Length 
 

class Addproduct(FlaskForm):
	name= StringField('Name:', validators=[DataRequired(), Length(min=2, max=100), Regexp('^[A-Za-z]*$', 0, 'Name must be only alphabeth')])
	price =  DecimalField('Price:', validators=[DataRequired(),
		Regexp('^[0-9.]*$', 0,'price must have only numbers')])
	discount = IntegerField('Discount:',  default=0)
	stock =  IntegerField('Stock:', validators=[DataRequired(),
		Regexp('^[0-9]*$', 0,'Mobile must have only numbers')])
	description =TextAreaField('Discription:', validators=[DataRequired(),
		Regexp('^[A-Za-z0-9" "]*$', 0, 'Description can only have combination of either alphabeth or number')])
	
	image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png', 'gif', 'jpeg'])])
	image_2 = FileField('Image 2', validators=[ FileAllowed(['jpg','png', 'gif', 'jpeg'])])
	image_3 = FileField('Image 3', validators=[ FileAllowed(['jpg','png', 'gif', 'jpeg'])])

	 