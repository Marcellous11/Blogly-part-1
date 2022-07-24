"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connects app to database."""

    db.app = app 
    db.init_app(app) 


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(20),nullable=False,)
    last_name = db.Column(db.String(30),nullable=False,)
    image_url = db.Column(db.String,nullable=False, default="https://plantbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=rhVwP3MG")
    

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,primary_key = True , autoincrement = True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    # created_at = db.Column(db.Date)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')