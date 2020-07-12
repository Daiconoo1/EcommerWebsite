from flask import render_template, session, url_for, redirect, request, flash, current_app
from flask_login import login_user, current_user, logout_user, login_required
from store import app, db, images, search, bcrypt, login, mail
from store.products.models import Brand, Category, AddProduct
from .models import CustomerRegister, CustomerOrder
from .forms import CustomrerSignupForm, CustomerLoginForm, ResetPasswordForm, RequestForm
import secrets, os
from sqlalchemy import func
from flask_mail import Message



@app.route ('/customersignup', methods=['GET','POST'])  
def customersignup():
	form = CustomrerSignupForm(request.form)	 
	if  form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash (form.password.data).decode('utf-8')
		customer =  CustomerRegister (name=form.name.data,email=form.email.data,address=form.address.data, 
			username=form.username.data, password=hashed_password, mobile=form.mobile.data )
		db.session.add (customer)
		db.session.commit()
		flash(f'Your accout has been created {form.username.data}! You can now log in','success') 		
		return redirect(url_for('customerlogin'))
	return render_template ('customer/customersignup.html', title='Customer Sign Up', form=form )


@app.route ('/customerlogin',methods=['GET','POST'] )
def customerlogin():
	 
	form = CustomerLoginForm(request.form)	
	if form.validate_on_submit():
		customer =CustomerRegister.query.filter_by(email=form.email.data).first()
		if customer and bcrypt.check_password_hash(customer.password, form.password.data):
			login_user(customer)			 
			flash(f'Welcome {form.email.data}! You are logged in', 'success')
			next_page = request.args.get('next')
			return redirect (next_page) if next_page else  redirect (url_for('index'))			 
		else:
			flash ('Your email or password is incorrect', 'danger')			
	return render_template('customer/customerlogin.html', form=form, title='Log In')

def send_reset_email(user):  
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f'''To reset your password, click on the link below:
{url_for('reset_token', token=token, _external=True)}

Ignore this email if you did not make the request
'''
	mail.send(msg)

@app.route('/requestpassword', methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))	
	form = RequestForm()
	if form.validate_on_submit():		 
		user = CustomerRegister.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash ('An email has been sent to you on how to reset your password', 'success')
		return redirect (url_for('customerlogin'))
	return render_template('customer/reset_request.html', form=form, title='Password Reset Request')

@app.route('/requestpassword/<token>', methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user= CustomerRegister.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token', 'danger')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if  form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash (form.password.data).decode('utf-8')
		user.password = hashed_password 		 
		db.session.commit()
		flash(f'Your password has been updated ! You can now log in','success')
		return redirect (url_for('customerlogin')) 		
	return render_template('customer/reset_token.html', form=form, title='Password Reset Request')

@app.route('/customerlogout')
def customerlogout():
	logout_user()
	return redirect (url_for('index'))
 

@app.route ('/getorder')
@login_required
def get_order():
	if current_user.is_authenticated:
		customer_id = current_user.id
		invoice = secrets.token_hex(3)
		try:
			order = CustomerOrder (invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
			db.session.add(order)
			db.session.commit()
			session.pop ('Shoppingcart')
			flash (f'Your order has been sent', 'success')			
			return redirect (url_for('orders', invoice=invoice))			 
		except Exception as e:
			print (e)
			flash (f'Order not delivered, Try again', 'danger')
			return redirect (url_for('getCart'))
		
@app.route ('/orders/<invoice>')
def orders(invoice):
	if current_user.is_authenticated:
		subtotal=0
		grandtotal = 0		 
		customer_id =current_user.id		 
		customer= CustomerRegister.query.filter_by(id=customer_id).first_or_404()
		order = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first_or_404()
		for key,product in order.orders.items():
			 
			d= ((float(product['Quantity']) * float(product['price'])))-((float(product['Quantity']) * float(product['price'])* float(product['discount']/100)))
			grandtotal = float ('%.2f' % (grandtotal+d))

	else:
		return redirect(url_for('customerlogin'))
	return render_template('customer/order.html', invoice=invoice, subtotal=subtotal, grandtotal=grandtotal,
		customer=customer, order=order)
 