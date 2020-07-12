import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from werkzeug.utils import secure_filename
from werkzeug import FileStorage
from flask_msearch import Search
from flask_login import LoginManager
from flask_mail import Mail
from flask_googlemaps import GoogleMaps


app = Flask(__name__) 
 

app.config['SECRET_KEY'] = 'd82e39598a65e096692a3d26fc6ac3dc' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
app.config['SECRET_KEY'] = 'd82e39598a65e096692a3d26fc6ac3dc'
db = SQLAlchemy(app)
 
bcrypt = Bcrypt(app)

basedir = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
UPLOAD_FOLDER = '/path/to/statics/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(basedir, 'static/images')

images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app)


search = Search()
search.init_app(app)

login = LoginManager()
login.init_app(app)
login.login_view='customerlogin'
login.login_view_message ='Please Login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oladimejiibrahim61@gmail.com' 
app.config['MAIL_DEFAULT_SENDER'] = 'oladimejiibrahim61@gmail.com' 
app.config['MAIL_PASSWORD'] = 'IBRAHIM24' 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
mail = Mail(app)

 
from store.admin import route
from store.products import route
from store.cart import route
from store.customer import route 
from store.api import route
 