"""Blogly application."""

from crypt import methods
from operator import methodcaller
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "secret"
app.config['DEBIG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def landing():
    
    return redirect('/user')

@app.route('/user')
def users():
    users = User.query.order_by('last_name').all()
    
    return render_template('all_users.html',users=users)

@app.route('/user/add')
def create_page():
    return render_template('create_user.html')

@app.route('/user/add', methods = ['POST'])
def add_user():
    """Add a new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    print(first_name)

    if image_url == '':
        image_url = 'https://plantbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=rhVwP3MG'

    user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f'/{user.id}')

  
@app.route('/<int:user_id>')
def show_user(user_id):
    """Show information about user """

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/<int:user_id>/edit")
def edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/<int:user_id>/edit", methods = ["POST"])
def edit_submit(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
   
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url 

    db.session.commit()
    return redirect(f'/{user.id}')

@app.route('/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):

    # user = User.query.get_or_404(user_id)

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/user')
