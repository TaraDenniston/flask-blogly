"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User

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
    return render_template("user-detail.html", user=user)

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
