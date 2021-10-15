"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@ app.route("/")
def home():
    return redirect("/users")


@ app.route("/users")
def users_home():
    """Shows list of all current users"""
    users = User.query.all()
    return render_template("users-home.html", users=users)


@ app.route("/users/new")
def render_user_form():
    """Renders form for creating a new user"""
    return render_template("add-user-form.html")


@ app.route("/users/new", methods=["POST"])
def add_user():
    """Handles data and new user creation"""
    # TO DO: get user data from form using request.form
    first_name = request.form["first_name"].capitalize()
    last_name = request.form["last_name"].capitalize()
    user_image = request.form["user_image"]
    new_user = User(first_name=first_name,
                    last_name=last_name, user_image=user_image)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@ app.route("/users/<int:user_id>/")
def render_user_details_page(user_id):
    """Loads user details page based on passed in user id"""
    found_user = User.query.get_or_404(user_id)
    return render_template("user-details-page.html", user=found_user)


@ app.route("/users/<int:user_id>/edit")
def render_user_edit_form(user_id):
    """Loads user edit form"""
    found_user = User.query.get_or_404(user_id)
    return render_template("user-edit-form.html", user=found_user)


@ app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_info(user_id):
    """Handles user edit data and modification"""
    found_user = User.query.get_or_404(user_id)
    found_user.first_name = request.form["first_name"]
    found_user.last_name = request.form["last_name"]
    found_user.user_image = request.form["user_image"]
    db.session.commit()
    return redirect(f"/users/{user_id}")


@ app.route("/users/<int:user_id>/delete/")
def delete_user(user_id):
    """Handles user deletion"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect(f"/users")

# ==========================POSTS ROUTES ==============================


@ app.route("/posts/<int:post_id>/")
def render_post_details_page(post_id):
    """Loads post details page"""
    found_post = Post.query.get_or_404(post_id)
    return render_template("post-details-page.html", post=found_post)


@ app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def handle_new_post(user_id):
    """handles new post operation"""
    if request.method == "GET":
        found_user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template("new-post-form.html", user=found_user, tags=tags)
    else:
        found_user = User.query.get_or_404(user_id)
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(title=request.form["post-title"],
                        content=request.form["post-content"], user=found_user, tags=tags)
        # TO DO: Handle tag association with post
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")


@ app.route("/posts/<int:post_id>/edit",  methods=["GET", "POST"])
def handle_post_edit(post_id):
    """handles post edit"""
    if request.method == "GET":
        found_post = Post.query.get_or_404(post_id)
        tags = Tag.query.all()
        return render_template("post-edit-form.html", post=found_post, tags=tags)
    else:
        found_post = Post.query.get_or_404(post_id)
        found_post.title = request.form["new-post-title"]
        found_post.content = request.form["new-post-content"]
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        found_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.add(found_post)
        db.session.commit()
        return redirect(f"/users/{found_post.user_id}")


@ app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Handles post deletion"""
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect("/users")

# ======================================= TAGS routes ===========================


@ app.route("/tags")
def all_tags_page():
    """renders all tags page"""
    tags = Tag.query.all()
    return render_template("tags-home-page.html", tags=tags)


@ app.route("/tags/<int:tag_id>")
def render_tag_details_page(tag_id):
    foundTag = Tag.query.get_or_404(tag_id)
    return render_template("tags-details-page.html", tag=foundTag)


@ app.route("/tags/new", methods=["GET", "POST"])
def handle_new_tags():
    if request.method == "GET":
        return render_template("new-tags-form.html")
    else:
        new_tag = Tag(name=request.form["tag-title"].capitalize())
        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def handle_tag_edits(tag_id):
    found_tag = Tag.query.get_or_404(tag_id)
    if request.method == "GET":
        return render_template("tags-edit-page.html", tag=found_tag)
    else:
        found_tag.name = request.form["tag-name"]
        post_ids = [int(num) for num in request.form.getlist("posts")]
        found_tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
        db.session.add(found_tag)
        db.session.commit()
        return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete")
def handle_tag_delete(tag_id):
    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()
    return redirect("/tags")

    # TO DO: Create an add tag link inside post details page.
    # TO DO: Create tag details page and allow to delete, edit current tag.
    # TO DO: Add a display on the post details page for its associated tags.
    # TO DO: Add a checkbox style form for different tags to add. As part of the edit post
    # and add post pages
