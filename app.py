"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'A2a`T2W8t@}#(tH8V2fg=bLC66e"|('


connect_db(app)
db.create_all()

@app.route('/')
def go_home():
    """Redirect to list of users""" 
    return redirect('/users')

@app.route('/users')
def home_page():
    """Show list of users""" 
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def add_form():
    """Display Create a User Form"""
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Add new user to database using form data"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # If no image was submitted, use a placeholder image
    if not image_url:
        image_url = 'https://via.placeholder.com/150'

    # If a user with the same first and last name already exists, flash a
    # message to the user and redirect back to the form
    if User.query.filter_by(first_name=first_name, last_name=last_name).one_or_none():
        flash('A user already exists by that name')
        return redirect('/users/new')

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user-detail.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """Display Edit a User Form"""
    return render_template('edit-user.html', user_id=user_id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Make updates to the database for an existing user using form data"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)

    # Only update info for fields that were not blank
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if image_url:
        user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from database and redirect to home page"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def display_post_form(user_id):
    """Display form to add a new post for the current user"""
    user = User.query.get(user_id)
    return render_template('new-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Add new post for current user to database using form data"""
    title = request.form['title']
    content = request.form['content']

    # If the form was submitted with any field blank, display a message
    if not title:
        flash('Please enter a title for your post')
        return redirect('/users/<int:user_id>/posts/new')
    if not content:
        flash('Please enter the content for your post')
        return redirect('/users/<int:user_id>/posts/new')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """Display a single post by a user"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template("post-detail.html", post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Display Edit Post Form"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    return render_template('edit-post.html', post=post, user_id=user_id)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Make updates to the database for an existing post using form data"""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id)

    # Only update info for fields that were not blank
    if title:
        post.title = title
    if content:
        post.content = content

    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post from database and redirect to user details page"""
    post = Post.query.get(post_id)
    user_id = post.user_id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')