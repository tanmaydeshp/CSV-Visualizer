from flask_sqlalchemy import *
from flask_login import UserMixin
from . import db 
from sqlalchemy.sql import func 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100))
    firstName = db.Column(db.String(250))
    lastName = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    files = db.relationship('File')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=func.now())
    filename = db.Column(db.String)
