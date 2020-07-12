import os
from .form import RegisterAdmint, AdminLoginForm
from flask import render_template, session, url_for, redirect, request, flash
from store import app, db, bcrypt
from .models import AdminUser
from store.products.models import AddProduct, Brand, Category
from store.customer.models import CustomerRegister, CustomerOrder


@app.route('/admin', methods=['POST', 'GET'])
def admin():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	product=AddProduct.query.all()
	return render_template ('admin/adminIndex.html', title='Admin Page', product=product)


@app.route('/avaiBrand', methods=['POST', 'GET'])
def avaiBrand():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	brand=Brand.query.all()
	return render_template ('admin/adminIndex.html', title='Avai. Brand', brand=brand)


@app.route('/avaiCat', methods=['POST', 'GET'])
def avaiCat():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	category=Category.query.all()
	return render_template ('admin/adminIndex.html', title='Avai. Category', category=category)

@app.route('/registeredcustomer', methods=['POST', 'GET'])
def registeredcustomer():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	customer=CustomerRegister.query.all()
	return render_template ('admin/adminIndex.html', title='Avai. Category', Customer=customer)


@app.route('/orderss', methods=['POST', 'GET'])
def orderss():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	subtotal=0
	grandtotal = 0
	customer_id = CustomerRegister.id
	customer = CustomerRegister.query.filter_by(id=customer_id).all()
	orders=CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).all()
	return render_template ('admin/adminIndex.html', title='Orders', customer=customer, Orders=orders, grandtotal=grandtotal)
 

@app.route('/regist', methods=['POST', 'GET'])
def register():
	if "adminemail"  in session:
		flash ('You have already registered', 'danger')
		return redirect (url_for('admin'))
	form=RegisterAdmint(request.form)
	if form.validate_on_submit() and request.method=='POST':
		hashed_password = bcrypt.generate_password_hash (form.password.data).decode('utf-8')
		admin =  AdminUser (name=form.name.data,adminemail=form.adminemail.data, username=form.username.data, 
			password=hashed_password, mobile=form.mobile.data )
		db.session.add (admin)
		db.session.commit()		 
		flash(f'Your accout has been created {form.username.data}! You are now able to log in','success')
		return redirect(url_for('adminlogin'))
	return render_template ('admin/Adminregister.html', form=form, title="Admin Register")

@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
	form = AdminLoginForm(request.form)
	if  form.validate() and request.method=="POST":
		admin =AdminUser.query.filter_by(adminemail=form.adminemail.data).first()
		if admin and bcrypt.check_password_hash(admin.password, form.password.data):
			session['adminemail']=form.adminemail.data
			flash(f'Welcome {form.adminemail.data}! You are logged in', 'success')
			next_page = request.args.get('next')
			return redirect (next_page) if next_page else  redirect (url_for('admin'))
		else:
			flash ('Your email or password is incorrect', 'danger')
	 
	return render_template ('admin/adminlogin.html', form=form, title="Admin Login")

@app.route('/adminlogout')
def adminlogout():
	session.pop('adminemail',None)
	return redirect (url_for('adminlogin'))
