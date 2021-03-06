 import os  
from flask import render_template, session, url_for, redirect, request, flash
from store import  app, db
from store.products.models import AddProduct
from store. customer.models import CustomerOrder
import simplejson
from decimal import Decimal
from flask_login import current_user, login_required
import stripe

publishable_key="pk_test_51H4CaZFfakTwIKt98iWYkwNeUu2tnnHMx5QnmWc0IzZpVL32PDlJlQfUkqe97nA8UjXjfdWEgzZB64dVdZTc5lDV00J65Y8ff6"

stripe.api_key= "sk_test_51H4CaZFfakTwIKt946RyK8a9MzpNYhTpVTeYHp9LGmJUwSERBj7dV8kAjB1CzcX8PXwaJHjfefFwD3BG7lrX0UX300Gauzc5Ld"

@app.route('/purchase', methods=['POST'])
@login_required
def purchase ():	 
	amount = request.form.get('amount')
	customer = stripe.Customer.create(
		email= request.form ['stripeEmail'],
		source=request.form['stripeToken'],
		)
	charge = stripe.Charge.create(
		customer=customer.id,
		description='Arc Boutique',
		amount= amount,
		currency='eur',
		)
	return redirect (url_for('success'))

@app.route('/success')
def success():
	return render_template ('customer/success.html')


def ManageDicts(dict1, dict2):
	if isinstance(dict1,list) and isinstance(dict2,list):
		return dict1 + dict2
	elif isinstance (dict1, dict) and isinstance(dict2,dict):
		return dict(list(dict1.items()) + list(dict2.items()))
	return False
		
@app.route('/addcart', methods=['POST', 'GET'])
def Addcart():	 
	try:
		product_id = request.form.get('product_id')
		Quantity = request.form.get('Quantity')
		product =AddProduct.query.filter_by(id=product_id).first()
		if product_id and   request.method=='POST':
			DictItems =  {product_id:{'name':product.name, 'price': Decimal(product.price), 'discount': Decimal(product.discount),
			'image':product.image_1, 'Quantity':Decimal(Quantity)}}			 
			if 'Shoppingcart' in session:				 
				print (session['Shoppingcart'])
				if product_id in session['Shoppingcart']:
					print ("This product is already added to cart")
				else:
					session['Shoppingcart'] = ManageDicts(session['Shoppingcart'],DictItems) 
					return redirect (request.referrer)

			else:
				session['Shoppingcart'] =DictItems
				return redirect('Addcart')




	except Exception as e:
		print(e)
	finally:
		return redirect(request.referrer) 

@app.route('/displaycart')
@login_required
def getCart():
	if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
		return redirect (url_for('index'))
	grandtotal = 0
	subtotal=0	 
	for key,product in session['Shoppingcart'].items():
		 
		subtotal += ((float(product['Quantity']) * float(product['price'])))-((float(product['Quantity']) * float(product['price'])* float(product['discount']/100)))
		grandtotal = ('%.2f' % (0+ float(subtotal)))
			 
	return render_template('products/displaycart.html', grandtotal=grandtotal)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def updatecart(id):
	if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
		return redirect(url_for('index'))
	if request.method == 'POST':
		Quantity= Decimal(request.form.get('Quantity'))
		try:
			session.modified = True
			for k, v in session['Shoppingcart'].items():
				if int(k) == id:
					v['Quantity'] = Quantity
					return redirect (url_for('getCart'))


		except Exception as e:
			print (e)
			return redirect (url_for('getCart'))


@app.route ('/delete/<int:ids>')
def deletecartItem(ids):
	if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
		return redirect(url_for('index'))
	try:
		session.modified = True
		for k, v in session['Shoppingcart'].items():
			if int(k) == ids:
				session['Shoppingcart'].pop(k, None)
				return redirect (url_for('getCart'))
		pass
	except Exception as e:
			print (e)
			return redirect (url_for('getCart'))
	
@app.route ('/clear')
def clearcart():
	session.pop ('Shoppingcart', None)
	return  redirect (url_for('index'))

