from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name='Alan', last_name='Alda', \
             image_url='https://pbs.twimg.com/profile_images/595641780768514048/umqK7iN5_400x400.jpg')
user2 = User(first_name='Joel', last_name='Burton', \
             image_url='https://www.rithmschool.com/assets/team/joel-a76cc6f1fb942e80144b05905493a2bf10a73adaab988df12a4abbb6762097bb.png')
user3 = User(first_name='Jane', last_name='Smith', \
             image_url='https://acultivatednest.com/wp-content/uploads/2018/06/should-you-be-like-an-old-fashioned-1950s-housewife-vintage-woman-artwork.jpg')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()