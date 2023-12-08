"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


#FIXME: ???? We have non nullable fields but we are still submitting blank
# form fields and its showing up as a blank (empty string?) in the DB
# it's not unknown but still empty....?
# DO required ? yes no

@app.get("/")
def index():
    """Redirects to list of users (homepage)."""

    return redirect('/users')

@app.get("/users")
def get_users():
    """Show all users with links to user-details and a link to add-user form."""

    users = User.query.all() #ordering (further study) #by user-id probably

    return render_template("/users/user_listing.html", users=users)

@app.get("/users/new")
def add_user():
    """Show an add form for users."""

    return render_template('/users/add_user_form.html')

@app.post("/users/new")
def handle_add_user_form():
    """Process the add form, adding a new user and redirecting back to /users"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    # image_url = request.form['image_url'] or None
    image_url = request.form.get('image_url', None)
    # image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    #flash new user created (visual confirmation)

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """
    Show information about the given user.
    Have a button to get to their edit page, and to delete the user.
    """

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)

    return render_template("/users/user_detail.html", user=user, posts=posts)

@app.get("/users/<int:user_id>/edit")
def edit_user_info(user_id):
    """
    Show the edit page for a user. Provides cancel button that returns to the
    detail page for a user, and a save button that updates the user.
    """

    user = User.query.get_or_404(user_id)
    return render_template("/users/user_edit.html", user=user)


@app.post("/users/<int:user_id>/edit")
def handle_edit_user_info_form(user_id):
    """
    Process the edit form, returning the user to the /users page.
    """

    user = User.query.get_or_404(user_id) #grabbing user object
    # what if database fails to return a user!?
    # probably better to handle exception but for now:
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    # user.image_url = request.form.get('image_url', None)
    user.image_url = request.form['image_url']
    # user.image_url = image_url if image_url else None
    # editing doesn't require "None"
    db.session.add(user)
    db.session.commit()

    #Flashing - user was edited

    return redirect("/users")

@app.post("/users/<user_id>/delete")
def handle_edit_user_delete_form(user_id):
    """Delete the user,, returning the user to the /users page."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    #flash user was deleted

    return redirect("/users")

"""Post routes: Users can add and edit posts on the blog"""

@app.get('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for that user
    """
    user = User.query.get_or_404(user_id)

    return render_template("/posts/add_post_form.html", user=user)

@app.post('/users/<int:user_id>/posts/new')
def handle_add_post(user_id):
    """Handle the add post form and redirect to the user detail page
    """

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,
                content=content,
                created_at=datetime.now(),
                user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    #flash new user created (visual confirmation)

    return redirect(f"/users/{user.id}")

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """ Show a post.
        Show buttons to edit and delete the post.
    """

    #not sure how the join with post/user is referenced here
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)

    return render_template("/posts/show_post.html", post=post, user=user)


@app.get('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)

    return render_template("/posts/edit_post.html", user=user, post=post)

@app.post('/posts/<int:post_id>/edit')
def handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    #Flashing - user was edited

    return redirect(f"/posts/{post_id}")


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    #flash user was deleted

    return redirect(f"/users/{post.user_id}")


