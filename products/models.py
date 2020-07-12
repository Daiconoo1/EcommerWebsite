from store import db
import json
from datetime import datetime 

class Brand (db.Model):
    __searchable__=['name']
    __tablename__ ='brand'     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)

     
class Category (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=False, nullable=False)


class AddProduct(db.Model):

    __searchable__=['name']   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Numeric(18,2), nullable=True)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    image_1=db.Column(db.String(200), nullable=True, default='pok.jpg')
    image_2=db.Column(db.String(200), nullable=True, default='pok.jpg')
    image_3=db.Column(db.String(200), nullable=True, default='pok.jpg')
    
    def __repr__(self):
        return f'AddProduct {self.name}' 



 
db.create_all()    

 