from unittest import TestCase

from app import app
from models import db, connect_db, User, Post

app.app_context().push()

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

connect_db(app)

# Reset test database before testing
db.drop_all()
db.create_all()


class UserViewsTest(TestCase):
    """Test view functions for users"""

    def setUp(self):
        """Add test users and posts"""

        # Delete any existing users/posts from database
        User.query.delete()
        Post.query.delete()

        # Create test users
        user1 = User(first_name="Cephalobot", \
                    last_name="the Octopus", \
                    image_url="https://dodo.ac/np/images/b/b5/Cephalobot_amiibo.png")
        user2 = User(first_name="Ribbot", \
                    last_name="the Frog", \
                    image_url="https://dodo.ac/np/images/thumb/9/94/Ribbot_NH.png/150px-Ribbot_NH.png")
        user3 = User(first_name="Sprocket", \
                    last_name="the Ostritch", \
                    image_url="https://dodo.ac/np/images/thumb/8/8b/Sprocket_NH.png/150px-Sprocket_NH.png")

        # Add test users to database
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        # Make test user ids available for test methods
        self.user1_id = user1.id
        self.user2_id = user2.id
        self.user3_id = user3.id

        # Create test posts
        post1 = Post(title="I'm the best", \
                    content="Nobody is better than me, donk donk.", \
                    user_id=self.user1_id)
        post2 = Post(title="Tips on Working Out", \
                    content="Never rest, never rust, zzrrbbit.", \
                    user_id=self.user2_id)
        post3 = Post(title="Life Advice", \
                    content="Strike while the iron is hot, zort.", \
                    user_id=self.user3_id)

        # Add test users to database
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

    def tearDown(self):
        """Make sure nothing is in the session before moving on to the next test"""

        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Cephalobot', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'first_name': 'Del', 'last_name': 'the Alligator', 'image_url': \
                 'https://dodo.ac/np/images/thumb/4/46/Del_NH.png/150px-Del_NH.png'}
            response = client.post('/users/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="my-3">Del the Alligator</h1>', html)

    def test_add_user_duplicate(self):
        with app.test_client() as client:
            d = {'first_name': 'Sprocket', 'last_name': 'the Ostritch', 'image_url': \
                 'https://dodo.ac/np/images/thumb/8/8b/Sprocket_NH.png/150px-Sprocket_NH.png'}
            response = client.post('/users/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('A user already exists by that name', html)

    def test_display_user(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user2_id}')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Ribbot the Frog', html)

    def test_delete_user(self):
        with app.test_client() as client:
            response = client.post(f'/users/{self.user1_id}/delete', follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('Cephalobot', html)


class PostViewsTest(TestCase):
    """Test view functions for posts"""

    def setUp(self):
        """Add test users and posts"""

        # Delete any existing users/posts from database
        User.query.delete()
        Post.query.delete()

        # Create test users
        user1 = User(first_name="Cephalobot", \
                    last_name="the Octopus", \
                    image_url="https://dodo.ac/np/images/b/b5/Cephalobot_amiibo.png")
        user2 = User(first_name="Ribbot", \
                    last_name="the Frog", \
                    image_url="https://dodo.ac/np/images/thumb/9/94/Ribbot_NH.png/150px-Ribbot_NH.png")
        user3 = User(first_name="Sprocket", \
                    last_name="the Ostritch", \
                    image_url="https://dodo.ac/np/images/thumb/8/8b/Sprocket_NH.png/150px-Sprocket_NH.png")

        # Add test users to database
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        # Make test user ids available for test methods
        self.user1_id = user1.id
        self.user2_id = user2.id
        self.user3_id = user3.id

        # Create test posts
        post1 = Post(title="I'm the best", \
                    content="Nobody is better than me, donk donk.", \
                    user_id=self.user1_id)
        post2 = Post(title="Tips on Working Out", \
                    content="Never rest, never rust, zzrrbbit.", \
                    user_id=self.user2_id)
        post3 = Post(title="Life Advice", \
                    content="Strike while the iron is hot, zort.", \
                    user_id=self.user3_id)

        # Add test users to database
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

        # Make test post ids available for test methods
        self.post1_id = post1.id
        self.post2_id = post2.id
        self.post3_id = post3.id

    def tearDown(self):
        """Make sure nothing is in the session before moving on to the next test"""

        db.session.rollback()

    def test_user_details_page(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user1_id}')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('the best', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {'title': 'Things I Like', 'content': \
                 'I kinda like having a Statue of Liberty on my jog route, zzrrbbitt', \
                 'user_id': 2}
            response = client.post('users/2/posts/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<a href="/posts/4">Things I Like</a>', html)

    def test_display_post(self):
        with app.test_client() as client:
            response = client.get(f'/posts/{self.post3_id}')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Strike while the iron is hot, zort.', html)

    def test_delete_post(self):
        with app.test_client() as client:
            response = client.post(f'/posts/{self.post1_id}/delete', follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('the best', html)