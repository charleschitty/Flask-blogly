"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db

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
    redirects to list of users
    """
    return redirect('/users')

@app.get("/users")
def get_users():
    """
    Show all users.
    Make these links to view the detail page for the user.
    Have a link here to the add-user form.
    """

    return render_template("/user_listing.html")

@app.get("/users/new")
def add_user():
    """
    Show an add form for users
    """

@app.post("/users/new")
def add_user():
    """
    Process the add form, adding a new user and going back to /users
    """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] #is there a command for like.get(x,None)
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(User)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<user-id>")
def show_user_info():
    """
    Show information about the given user.

    Have a button to get to their edit page, and to delete the user.
    """

@app.get("/users/<user-id>/edit")
def edit_user_info():
    """
    Show the edit page for a user.

    Have a cancel button that returns to the detail page for a user,
    and a save button that updates the user.
    """

@app.post("/users/<user-id>/edit")
def handle_edit_user_info_submit():
    """
    Process the edit form, returning the user to the /users page.
    """

@app.post("/users/<user-id>/delete")
def handle_edit_user_info_submit():
    """
    Delete the user
    """
