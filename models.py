from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean(128),default=False)
    is_approved = db.Column(db.Boolean(128),default=False)
    password = db.Column(db.String(128),nullable=False)

    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False) 


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)   