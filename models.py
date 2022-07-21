"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(20),nullable=False,)
    last_name = db.Column(db.String(30),nullable=False,)
    image_url = db.Column(db.String,nullable=False, default="https://plantbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=rhVwP3MG")
    
def connect_db(app):
    """Connects app to database."""

    db.app = app 
    db.init_app(app) 
