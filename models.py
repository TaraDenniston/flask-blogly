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

    posts = db.relationship('Post', back_populates='user')

    def __repr__(self):
        return f'User {self.id}: {self.first_name} {self.last_name}'
    
    def full_name(self):
        """Return a string with the user's full name"""
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post model - a post is an article written by a user"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    user = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary='posts_tags', back_populates='posts')
    
    def __repr__(self):
        return f'Post {self.id}: "{self.title}" created at {self.created_at}'

class Tag(db.Model):
    """Tag model - a tag is a label or category"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                     unique=True,
                     nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', back_populates='tags')

    def __repr__(self):
        return f'Tag {self.id}: {self.name}'

class PostTag(db.Model):
    """PostTag model - multiple tags can be connected to each post, and each 
    post can have multiple tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id', ondelete='CASCADE'),
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id', ondelete='CASCADE'),
                       primary_key=True)



    

