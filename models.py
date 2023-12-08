"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/default-url-image"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

#where did inputs come from - ex: provided by user -required data
class User(db.Model):
    """User

    Fields:
    - id (serial)
    - first_name
    - last_name
    - image_url
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name =  db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        default = DEFAULT_IMAGE_URL
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} id={self.id}>"


class Post(db.Model):
    """
    Fields:
        id int PK
        title str
        content str
        created_at date with time zone and time stamp
        user_id FK users

    """
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(100),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable = False)

    created_at = db.Column(
        db.DateTime,
        nullable=False
    )
    #Do we need Nullable on user_id (both arguments)
    #preserve post history but remove user (reddit by <deleted>)
    #or data/privacy reasons: delete whole-sale when user requests data deletion
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.title} {self.created_at} {self.id}>"





