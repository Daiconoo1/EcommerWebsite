from flask import render_template, session, url_for, redirect, request, flash, current_app
from store import app, db, images, search
from .models import Brand, Category, AddProduct 
from .forms import Addproduct
import secrets, os
from sqlalchemy import func
from flask import send_from_directory


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
	return render_template ('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('error/500.html'), 500

@app.route('/', methods=['POST','GET'])
def index ():
	page = request.args.get('page', 1, type=int)
	brand=Brand.query.all()
	category=Category.query.all()
	product=AddProduct.query.order_by(func.random()).filter(AddProduct.stock>0).paginate(page=page, per_page=12)
	slid =AddProduct.query.order_by(func.random()).limit(4) 
	slide=AddProduct.query.order_by(func.random()).limit(5)
	return render_template('main/index.html', brands=brand, Slickky=slid, Slick=slide, Category=category,
		Products=product, title='Index Page')

@app.route('/brand/<int:id>', methods=['POST', 'GET'])
def getbrand(id):	 
	getbrand=Brand.query.filter_by(id=id).first()
	brandd=Brand.query.all()
	brand=AddProduct.query.filter_by(brand=getbrand).all()	
	return render_template ('products/brand.html', brands=brand, brandss=brandd)

@app.route('/cat/<int:id>', methods=['POST', 'GET'])
def getcat(id):
	brand=Brand.query.all()
	getcat=Brand.query.filter_by(id=id).first()	
	category=AddProduct.query.filter_by(category=getcat).all()
	cat=Category.query.all()
	slid =AddProduct.query.order_by(func.random()).limit(4) 
	slide=AddProduct.query.order_by(func.random()).limit(5)	
	return render_template ('main/index.html', category=category, brands=brand, Category=cat, 
		Slickky=slid, Slick=slide)

@app.route('/detailed/<int:id>', methods=['POST', 'GET'])
def detailedpage(id):
	category=Category.query.all()
	brand =Brand.query.all()
	product = AddProduct.query.get(id)
	return render_template('products/detailedpage.html', Category=category, product=product, brand=brand)

@app.route('/search' )
def search():		 
	brand = Brand.query.all()
	keyword = request.args.get('query')	 
	results = (AddProduct.query.msearch(keyword, fields=['name']).filter(AddProduct.stock > 0))
	return render_template('products/searchesult.html', results=results, brands=brand)
	 


@app.route ('/addnewbrand', methods=['POST', 'GET'])
def addnewbrand():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	brands= Brand()
	if request.method=='POST':
		getbrand = request.form.get('bran')
		bran = Brand (name = getbrand)
		db.session.add (bran)
		flash (f'The Brand {getbrand} has been added', 'success')
		db.session.commit()
		return redirect (url_for('addnewbrand'))
	return render_template ('products/addnewbrand.html', title='Add Brand', brands=brands )

@app.route('/editBrand/<int:id>', methods=['POST','GET'])
def editBrand(id):
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	editbrand= Brand.query.get(id)
	brand = request.form.get('bran')
	if request.method=='POST':
		 editbrand.name = brand
		 flash ('Brand has been updated', 'success')
		 db.session.commit()
		 return redirect (url_for('avaiBrand'))
	return render_template ('products/editbrand.html', title='Edit Brand', editbrand=editbrand)

@app.route('/deletebrand/<int:id>', methods=['POST', 'GET'])
def deletebrand(id):
	brand=Brand.query.get_or_404(id)	 
	if request.method=='POST':		 
		db.session.delete(brand)
		db.session.commit()
		flash (f'{brand.name} as been successfully deleted', 'success')
		return redirect(url_for('avaiBrand'))
	flash (f'{brand.name} can not delete', 'danger')
	return redirect(url_for('avaiBrand'))
	


@app.route ('/addnewcat', methods=['POST', 'GET'])
def addnewcat():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	
	category = Category()
	if request.method=='POST':
		getcat = request.form.get('cat')
		cat = Category (name = getcat)
		db.session.add (cat)
		flash (f'The Category {getcat} has been added', 'success')
		db.session.commit()
		return redirect (url_for('addnewcat'))
	return render_template ('products/addnewbrand.html', title='Add Category', category=category )


@app.route('/editCat/<int:id>', methods=['POST','GET'])
def editCat(id):
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))
	editcat= Category.query.get(id)
	category = request.form.get('cat')
	if request.method=='POST':
		 editcat.name = category
		 flash ('Category has been updated', 'success')
		 db.session.commit()
		 return redirect (url_for('avaiCat'))
	return render_template ('products/editbrand.html', title='Edit Brand', editcat=editcat)


@app.route('/deletecat/<int:id>', methods=['POST', 'GET'])
def deletecat(id):
	cat=Category.query.get_or_404(id)	 
	if request.method=='POST':		 
		db.session.delete(cat)
		db.session.commit()
		flash (f'{cat.name} as been successfully deleted', 'success')
		return redirect(url_for('avaiCat'))
	flash (f'{cat.name} can not delete', 'danger')
	return redirect(url_for('avaiCat'))

@app.route ('/addproduct', methods=['POST', 'GET'])
def addnewproduct():
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))	 
	brand = Brand.query.all()
	category = Category.query.all()
	form = Addproduct()
	if request.method == 'POST':
		image_1=images.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
		image_2=images.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
		image_3=images.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
		addprt = AddProduct(name=form.name.data, price =form.price.data, discount=form.discount.data, stock=form.stock.data,
			description=form.description.data, brand_id=request.form.get('brand'), category_id=request.form.get('category'), 
			image_1=image_1,image_2=image_2, image_3=image_3)
		db.session.add(addprt)
		flash('Product has been added successfully to the database', 'success')
		db.session.commit()
		return redirect(url_for('addnewproduct'))
	return render_template ('products/addnewproduct.html', title='Add Product', form=form, brands=brand, 
		Category=category )

@app.route ('/editProduct/<int:id>', methods=['POST','GET'])
def editProduct (id):
	if "adminemail" not in session:
		flash ('You have to login first', 'danger')
		return redirect (url_for('adminlogin'))	
	form=Addproduct(request.form)
	editproduct= AddProduct.query.get(id)	 
	category = Category.query.all()
	brand = Brand.query.all()
	brands = request.form.get('brand')
	categorys = request.form.get('category')
	if request.method=='POST':
		editproduct.name=form.name.data
		editproduct.price=form.price.data
		editproduct.discount=form.discount.data
		editproduct.stock = form.stock.data
		editproduct.description=form.description.data
		editproduct.brand_id=brands
		editproduct.category_id=categorys
		if request.files.get('image_1'):
			if request.files.get('image_1'):
				try:
					os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_1))
					editproduct.image_1=images.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
				except:
					editproduct.image_1=images.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
			elif request.files.get('image_2'):
				try:
					os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_2))
					editproduct.image_2=images.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
				except:
					editproduct.image_3=images.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
			elif request.files.get('image_3'):
				try:
					os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_3))
					editproduct.image_3=images.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
				except:
					editproduct.image_3=images.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
			else:
				flash('Image not in database')			 
		db.session.commit()

		flash ('Product has been updated', 'success')
		return redirect (url_for('admin')) 

	form.name.data= editproduct.name
	form.price.data= editproduct.price
	form.discount.data= editproduct.discount
	form.stock.data= editproduct.stock
	form.description.data= editproduct.description
	return render_template ('products/editbrand.html', title='Edit Product', editproduct=editproduct, brand=brand,
		category=category, form=form)

@app.route('/deleteproduct/<int:id>', methods=['POST','GET'])
def deleteproduct(id):
	product=AddProduct.query.get(id)
	if request.method=='POST':
		try:
			os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_1))
			os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_2))
			os.unlink(os.path.join(current_app.root_path,'static/images/' + editproduct.image_3))
		except Exception as e:
			print (e)		 
		db.session.delete(product)
		db.session.commit()
		flash (f'{product.name} has been deleted', 'success')
		return redirect (url_for('admin'))
	flash (f'{product.name} can not be delete', 'success')
	return redirect (url_for('admin'))


 