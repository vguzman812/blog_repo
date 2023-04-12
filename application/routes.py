"""Route declaration."""

from flask import render_template, url_for, redirect, Blueprint, session, flash
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User, BlogPost, Comment
from . import login_manager
from flask_login import current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, CommentForm, ContactForm
from .assets import compile_static_assets

from functools import wraps

# Blueprint Configuration
main_bp = Blueprint(
	'main_bp',
	__name__,
	template_folder='templates',
	static_folder='static'
)


# home page
@main_bp.route('/')
def index():
	# posts = BlogPost.query.all()
	return render_template("index.html", current_user=current_user)


# generic page
@main_bp.route('/generic')
def generic():
	return render_template("generic.html")


# example of elements with scss styling to add to other pages as needed
@main_bp.route('/elements')
def elements():
	return render_template("elements.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
	"""Standard `contact` form."""
	form = ContactForm()
	if form.validate_on_submit():
		return redirect(url_for("success"))
	return render_template(
		"contact.html",
		form=form,
		template="form-template"
	)


@main_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main_bp.index'))


@main_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
	form = CommentForm()
	requested_post = BlogPost.query.get(post_id)

	if form.validate_on_submit():
		if not current_user.is_authenticated:
			flash("You need to login or register to comment.")
			return redirect(url_for("auth_bp.login"))

		new_comment = Comment(
			text=form.comment_text.data,
			comment_author=current_user,
			parent_post=requested_post
		)
		db.session.add(new_comment)
		db.session.commit()

	# TODO: Change this in the future to post.html
	return render_template("generic.html", post=requested_post, form=form, current_user=current_user)


# route for photo uploads for the post. TODO: Fix this to use in post creation:
#  https://flask-wtf.readthedocs.io/en/1.0.x/form/#file-uploads
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     form = PhotoForm()
#
#     if form.validate_on_submit():
#         f = form.photo.data
#         filename = secure_filename(f.filename)
#         f.save(os.path.join(
#             app.instance_path, 'photos', filename
#         ))
#         return redirect(url_for('index'))
#
#     return render_template('upload.html', form=form)


@main_bp.route('/user/<username>')
def profile(username):
	# Logic goes here
	pass
