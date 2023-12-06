"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db
from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.get("/")
def index():
    """
    Creates homepage HTML.
    """

    return render_template("homepage.html")
    """It should be able to import the User model, and create the
    tables using SQLAlchemy. Make sure you have the FlaskDebugToolbar
    installed — it’s especially helpful when using SQLAlchemy."""

@app.post("/")
def add_user():
    """
    Add user and redirect to list of users
    """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] #is there a command for like.get(x,None)
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(User)
    db.session.commit()

    return redirect(f"/{user.id}")

