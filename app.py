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
def home_page():
    """Show home page with list of users""" 
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/new-user')
def add_form():
    """Display Create a User Form"""
    return render_template('new-user.html')

@app.route('/new-user', methods=['POST'])
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
        return redirect('/new-user')

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/{user.id}')

@app.route('/<int:user_id>')
def display_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)
