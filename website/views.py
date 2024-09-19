"""This module contains the views for the website. 
It includes routes for the home page, review page,
creating and deleting posts, liking posts,
viewing user's posts, creating and deleting comments, 
and managing user account details.
The views are implemented using the Flask framework
and interact with the database through SQLAlchemy.
Authentication and authorization are handled using Flask-Login.
The module also includes forms for updating account details and changing passwords.
"""


# Necessary imports for the views module
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Like, Comment
from .forms import UpdateAccountForm, ChangePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Creates a Blueprint for the views
views = Blueprint("views", __name__)

# Route for Home page
@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user)


# Route to view reviews page
@views.route("/review")
@login_required
def review():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("review.html", user=current_user, posts=posts)


# CREATE POST
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Review posted!', category='success')
            return redirect(url_for('views.review'))
    return render_template('create_review.html', user=current_user)


# Like Post
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


# Check certain user's posts
@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(
        author=user.id).paginate(page=page, per_page=4)

    return render_template("user_reviews.html", user=current_user, posts=posts, username=username)


# Delete Post
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted,', category='success')
    return redirect(url_for('views.review'))


# Create Comment
@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment posted!', category='success')
        else:
            flash('Post does not exist', category="error")
    return redirect(url_for('views.review'))


# Delete Comment
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        flash('Comment deleted!', category='success')
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.review'))

# Route to view account page and edit account details
@views.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated!', category='success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        flash('Invalid username or email, please try again.', category='error')
    return render_template('account.html', user=current_user, form=form)

# Route for changing password
@views.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Verifying the old password
        if check_password_hash(current_user.password, form.old_password.data):
            # Hashes the new password before committing to database
            hashed_password = generate_password_hash(
                (form.new_password.data), method='pbkdf2:sha256')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password succesfully changed!', category='success')
            return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.old_password.data = ''

    return render_template('change_password.html', user=current_user, form=form)
