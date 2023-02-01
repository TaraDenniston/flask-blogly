"""Blogly application."""

from flask import Flask, render_template, request, redirect
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
    """Shows home page with list of users""" 
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/new-user')
def add_form():
    """Displays Create a User Form"""
    return render_template('new-user.html')

@app.route('/new-user', methods=['POST'])
def add_user():
    """Adds new user to database using form data"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/{user.id}')
