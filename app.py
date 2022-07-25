"""Blogly application."""

from crypt import methods
from operator import methodcaller
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['TESTING'] = True
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
    """Will redirect you to landing page"""
    return redirect('/user')


@app.route('/user')
def users():
    """Takes you to landing page with list of users"""
    users = User.query.order_by('last_name').all()
    return render_template('all_users.html',users=users)


@app.route('/user/add')
def create_page():
    """A form where you can add users"""
    return render_template('create_user.html')


@app.route('/user/add', methods = ['POST'])
def add_user():
    """Path where new users are submitted"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    print(first_name)

    if image_url == '':
        image_url = 'https://plantbiology.ucr.edu/sites/default/files/styles/form_preview/public/blank-profile-pic.png?itok=rhVwP3MG'

    user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f'/user/{user.id}')

  
@app.route('/user/<int:user_id>')
def show_user(user_id):
    """Show information about user """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(User.id==2)
    return render_template("user_details.html", posts=posts, user=user)


@app.route("/user/<int:user_id>/edit")
def edit_page(user_id):
    """Form where you can edit user information"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route("/user/<int:user_id>/edit", methods = ["POST"])
def edit_submit(user_id):
    """Path where user edits are submitted """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
   
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url 

    db.session.commit()
    return redirect(f'/user/{user.id}')


@app.route('/user/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Delete a user profile"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/user')


@app.route('/user/<int:user_id>/add_post')
def add_post_form(user_id):
    """form to add a new user post"""
    user = User.query.get_or_404(user_id)
    return render_template('add_post.html',user=user)


@app.route('/user/<int:user_id>/add_post', methods = ['POST'])
def add_post(user_id):
    """Where new user post is submitted"""
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    post = Post(title=title,content=content,users_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/user/{user_id}/post_details/{post.id}' )


@app.route('/user/<int:user_id>/post_details/<int:post_id>')
def post_detaisl(user_id,post_id):
    """Information about user post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html',user=user,post=post)


@app.route('/user/<int:user_id>/post_details/<int:post_id>/edit')
def edit_post(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html',user=user,post=post)

    
@app.route("/user/<int:user_id>/post_details/<int:post_id>/edit", methods = ["POST"])
def edit_post_submit(user_id,post_id):
    """Path where user edits are submitted """
    title = request.form['title']
    content = request.form['content']
    
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.commit()
    return redirect(f'/user/{user_id}/post_details/{post_id}')


@app.route('/user/<int:user_id>/post_details/<int:post_id>/delete', methods = ['POST'])
def delete_post(user_id,post_id):
    """Delete a user profile"""
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/user/{user_id}')