import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )
        db.session.add(test_user)
        db.session.commit()


        test_post = Post(
            title="test1_title",
            content="test1_content",
            user_id=test_user.id,
            created_at='2023-12-07 07:49:02.747421'
        )


        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

       # breakpoint()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests if manually added user found on user list homepage"""
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_add_users(self):
        """Tests if form added user found on user list homepage"""

        with app.test_client() as c:

            data = {
                "first_name": "Joel",
                "last_name": "Burton",
                "image_url": None
            }

            # test full user and no image user

            resp = c.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Joel", html)
            self.assertIn("Burton",html)
            self.assertIn("Users List", html)


    def test_load_user_detail_page(self):
        """
        Tests that the user detail page loads correctly
        """

        with app.test_client() as c:

            # test_user = User.query.get(self.user_id)

            resp = c.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            # self.assertIn(test_user.first_name, html)
            self.assertIn("test1_first",html)
            # self.assertIn(test_user.last_name, html)
            self.assertIn("test1_last",html)
            self.assertIn("User: test1_first test1_last", html)
            # self.assertIn(f"User: {test_user.first_name} {test_user.last_name}",
            #  html)

    def test_edit_users(self):
        """Tests if form edited user found on user list homepage"""

        with app.test_client() as c:

            test_user = User.query.get(self.user_id)
            test_user.last_name = "test_Burton"

            #test a bunch of edits
            data = {
                "first_name" : test_user.first_name,
                "last_name" : test_user.last_name,
                "image_url" : test_user.image_url,
            }

            resp = c.post(f"/users/{self.user_id}/edit",
                          data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            # self.assertIn(test_user.first_name, html)
            self.assertIn("test_Burton",html)
            # self.assertIn(test_user.last_name, html)
            self.assertIn("Users List", html)


    def test_delete_users(self):
        """Tests if deleted user removed from user homepage"""

        with app.test_client() as c:

            # test_user = User.query.get(self.user_id)

            resp = c.post(f"/users/{self.user_id}/delete",
                           follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            # self.assertNotIn(test_user.first_name, html)
            self.assertNotIn("test1_last",html)
            # self.assertNotIn(test_user.last_name, html)
            self.assertIn("Users List", html)


    """ TESTS FOR POSTS"""

    def test_list_post(self):#FIXME: what
        """Tests posts show up on user detail page"""
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)

            self.assertIn("test1_title", html)

    # def test_add_users(self):
    #     """Tests if form added user found on user list homepage"""

    #     with app.test_client() as c:

    #         data = {
    #             "first_name": "Joel",
    #             "last_name": "Burton",
    #             "image_url": None
    #         }

    #         # test full user and no image user

    #         resp = c.post("/users/new", data=data, follow_redirects=True)
    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("Joel", html)
    #         self.assertIn("Burton",html)
    #         self.assertIn("Users List", html)


    # def test_load_user_detail_page(self):
    #     """
    #     Tests that the user detail page loads correctly
    #     """

    #     with app.test_client() as c:

    #         # test_user = User.query.get(self.user_id)

    #         resp = c.get(f"/users/{self.user_id}")
    #         html = resp.get_data(as_text=True)
    #         # self.assertIn(test_user.first_name, html)
    #         self.assertIn("test1_first",html)
    #         # self.assertIn(test_user.last_name, html)
    #         self.assertIn("test1_last",html)
    #         self.assertIn("User: test1_first test1_last", html)
    #         # self.assertIn(f"User: {test_user.first_name} {test_user.last_name}",
    #         #  html)

    # def test_edit_users(self):
    #     """Tests if form edited user found on user list homepage"""

    #     with app.test_client() as c:

    #         test_user = User.query.get(self.user_id)
    #         test_user.last_name = "test_Burton"

    #         #test a bunch of edits
    #         data = {
    #             "first_name" : test_user.first_name,
    #             "last_name" : test_user.last_name,
    #             "image_url" : test_user.image_url,
    #         }

    #         resp = c.post(f"/users/{self.user_id}/edit",
    #                       data=data, follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("test1_first", html)
    #         # self.assertIn(test_user.first_name, html)
    #         self.assertIn("test_Burton",html)
    #         # self.assertIn(test_user.last_name, html)
    #         self.assertIn("Users List", html)


    # def test_delete_users(self):
    #     """Tests if deleted user removed from user homepage"""

    #     with app.test_client() as c:

    #         # test_user = User.query.get(self.user_id)

    #         resp = c.post(f"/users/{self.user_id}/delete",
    #                        follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertNotIn("test1_first", html)
    #         # self.assertNotIn(test_user.first_name, html)
    #         self.assertNotIn("test1_last",html)
    #         # self.assertNotIn(test_user.last_name, html)
    #         self.assertIn("Users List", html)
