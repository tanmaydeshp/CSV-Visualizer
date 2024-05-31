from flask import Flask
from os import path, urandom 
from flask_sqlalchemy import *
from flask_login import *
import os 

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(32).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    if not path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    from .views import views
    from .auth import auth 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') 
    from .models import User
    create_db(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists(path.join("app\\", DB_NAME)): 
        with app.app_context():
            db.create_all()