"""Blogly application."""

from crypt import methods
from operator import methodcaller
from flask import Flask, request, redirect, render_template, request_started
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post , Tag, PostTag

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
    tags = Tag.query.filter(Tag.id > 0).all()
    return render_template('all_users.html',users=users,tags=tags)


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
    posts = Post.query.filter(User.id > 0)
    
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
    tags = Tag.query.filter(Tag.id > 0).all()
    return render_template('add_post.html',user=user,tags=tags)


@app.route('/user/<int:user_id>/add_post', methods = ['POST'])
def add_post(user_id):
    """Where new user post and asigns tags is submitted"""
    title = request.form['title']
    content = request.form['content']
    tag_id_list = request.form.getlist('tag')
    user = User.query.get_or_404(user_id)
    post = Post(title=title,content=content,users_id=user_id)

    db.session.add(post)
    db.session.commit()


    curr_post = len(Post.query.filter(User.id > 0).all() )
    for tag_id in tag_id_list:
        posttag = PostTag(post_id=curr_post, tag_id=tag_id)
        db.session.add(posttag)
        db.session.commit()

  
    return redirect(f'/user/{user_id}/post_details/{post.id}' )


@app.route('/user/<int:user_id>/post_details/<int:post_id>')
def post_detaisl(user_id,post_id):
    """Information about user post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    
    return render_template('post_details.html',user=user,post=post,tags=tags)


@app.route('/user/<int:user_id>/post_details/<int:post_id>/edit')
def edit_post(user_id, post_id):
    """Edit a post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.filter(Tag.id > 0).all()


    checked_tags = post.tags
    return render_template('edit_post.html',user=user,post=post,all_tags=all_tags,checked_tags=checked_tags)

    
@app.route("/user/<int:user_id>/post_details/<int:post_id>/edit", methods = ["POST"])
def edit_post_submit(user_id,post_id):
    """Path where user edits are submitted """
    post = Post.query.get_or_404(post_id)
    post.tags.clear()
    db.session.commit()

    title = request.form['title']
    content = request.form['content']
    tag_id_list = request.form.getlist('tag')
    
    post.title = title
    post.content = content

    for tag_id in tag_id_list:
        posttag = PostTag(post_id=post_id, tag_id=tag_id)
        db.session.add(posttag)
        db.session.commit()

    db.session.commit()
    return redirect(f'/user/{user_id}/post_details/{post_id}')


@app.route('/user/<int:user_id>/post_details/<int:post_id>/delete', methods = ['POST'])
def delete_post(user_id,post_id):
    """Delete a user profile"""

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/user/{user_id}')


@app.route('/user/add_tags')
def tags():
    """This is the form to create a new tag"""

    tags = Tag.query.filter(Tag.id > 0).all()
    return render_template('add_tags.html',tags=tags)

@app.route('/user/add_tags', methods=['POST'])
def create_tags():
    """Submission to creating a new tag"""
    name = request.form['name']
    tag = Tag(name=name) 
    db.session.add(tag)
    db.session.commit()
    return redirect('/user')


@app.route('/user/tag/<int:tag_id>')
def show_post_of_tags(tag_id):
    """Shows a list of post related to a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts_list = tag.post
    
    return render_template('show_related_post.html', tag=tag,posts_list=posts_list)


@app.route('/user/tag/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    
    return render_template('edit_tag.html', tag=tag)

@app.route('/user/tag/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    tag_name = request.form['name']

    tag.name = tag_name
    db.session.commit()
    return redirect(f'/user/tag/{tag_id}')

@app.route('/user/tag/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/user')
