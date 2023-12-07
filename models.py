"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User.

    Fields:
    -dept_code: xxx
    -dept_name: yyy

    Relationship:
    -employees : returns lsit of [EmployeeInstnace, ...]
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
        db.Text
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} id={self.id}>"
