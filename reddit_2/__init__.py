from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import configure_uploads, IMAGES, UploadSet

app = Flask(__name__, static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reddit_2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'efce6a1f8c24fc662b5fb089'
app.config['UPLOADED_IMAGES_DEST'] = './static/media'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from reddit_2 import routes