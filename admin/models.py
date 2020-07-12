from store import db
 
 

 
class AdminUser(db.Model):
	__tablename__='adminuser'	 
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=False, nullable=False)
	adminemail = db.Column(db.String(120), unique=True, nullable=False)
	username = db.Column(db.String(20), unique=False, nullable=False)	
	password = db.Column(db.String(60),  nullable=False)	 
	mobile = db.Column(db.Integer, nullable=False )
	profile = db.Column(db.String(220), unique=False, nullable=False, default='pok.jpg')
	
	def __repr__(self):
		return '<AdminUser %r>' % self.username
	  
	
db.create_all()


