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
