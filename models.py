"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50))
    image_url = db.Column(db.String, default='https://via.placeholder.com/150')

    def __repr__(self):
        return f'User {self.id}: {self.first_name} {self.last_name}'
    
    def full_name(self):
        """Return a string with the user's full name"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
    
    def __repr__(self):
        return f'Post {self.id}: "{self.title}" created at {self.created_at}'

