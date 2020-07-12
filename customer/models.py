from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from store import db, login
import json
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def user_loader(user_id):
	return CustomerRegister.query.get(user_id) 
	

class CustomerRegister(db.Model, UserMixin):
	__tablename__='user'	 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	address = db.Column(db.String(220), unique=False, nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)	
	password = db.Column(db.String(60),  nullable=False)	 
	mobile = db.Column(db.Integer, nullable=False )	 
	date_created =db.Column (db.DateTime, default=datetime.utcnow, nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer( 'd82e39598a65e096692a3d26fc6ac3dc', expires_sec )
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer('d82e39598a65e096692a3d26fc6ac3dc')
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return CustomerRegister.query.get(user_id)   

	def is_active(self):
		return True

	

	def __repr__(self):
		return "<Register %r>" % self.name


class JsonEncodedDict(db.TypeDecorator):
	impl = db.Text

	def process_bind_param (self, value, dialect):
		if value is None:
			return '[]'
		else:
			return json.dumps(value)
	def process_result_value(self, value, dialect):
		if value is None:
			return '[]'
		else:
			return json.loads(value)


class CustomerOrder(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	invoice =db.Column (db.String(20), unique=True, nullable=False)
	status =db.Column (db.String(20), default='Pending',  nullable=False)
	customer_id =db.Column(db.Integer,  nullable=False)
	date_created =db.Column (db.DateTime, default=datetime.utcnow, nullable=False)
	orders =db.Column (JsonEncodedDict)

	def __repr__(self):
		return '<CustomerOrder %r>' % self.invoice


db.create_all()