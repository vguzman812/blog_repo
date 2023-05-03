"""Route declaration."""

from flask import render_template, url_for, redirect, Blueprint, session, flash, request
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User, BlogPost, Comment
from . import login_manager
from flask_login import current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, CommentForm, ContactForm, CreatePostForm
from .assets import compile_static_assets

from functools import wraps

# Blueprint Configuration
main_bp = Blueprint(
	'main_bp',
	__name__,
	template_folder='templates',
	static_folder='static'
)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


# #Internal server error
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


# home page
@main_bp.route('/')
def index():
	posts = BlogPost.query.all()
	page = request.args.get('page', 1, type=int)
	pagination = BlogPost.query.order_by(BlogPost.created_on.desc()).paginate(page=page, per_page=6)

	return render_template(
		"index.html",
		current_user=current_user,
		pagination=pagination,
		all_posts=posts,
	)


@main_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
	"""
		Rendering page for requested post.

		GET requests serve requested post.
		POST requests validate and commits comment to post.
	"""
	form = CommentForm()
	requested_post = BlogPost.query.get_or_404(post_id)
	author = User.query.get(requested_post.author_id)

	if form.validate_on_submit():
		if not current_user.is_authenticated:
			flash("You need to login to comment.")
			return redirect(url_for("main_bp.post", post_id=post_id))

		new_comment = Comment(
			text=form.comment_text.data,
			author_id=current_user.id,
			post_id=form.post_id.data,
			created_on=dt.utcnow(),
		)
		db.session.add(new_comment)
		db.session.commit()
		return redirect(url_for('main_bp.post', post_id=post_id))

	return render_template(
		"post.html",
		post=requested_post,
		author=author,
		form=form,
		current_user=current_user,
	)


@main_bp.route('/create_post', methods=["GET", "POST"])
@login_required
def create_post():
	"""
		Page for creating posts for registered users

		GET requests serve creation form.
		POST requests validate and commits new post to database.
	"""
	form = CreatePostForm()
	if form.validate_on_submit():
		flash('Post successfully created')
		new_post = BlogPost(
			title=form.title.data,
			subtitle=form.subtitle.data,
			body=form.body.data,
			img_url=form.img_url.data,
			author=current_user,
			author_id=current_user.id,
			created_on=dt.today()
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("main_bp.post", post_id=new_post.id))
	return render_template(
		"create_post.html",
		form=form,
		current_user=current_user,
	)


@main_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
	post = BlogPost.query.get_or_404(post_id)
	form = CreatePostForm(
		title=post.title,
		subtitle=post.subtitle,
		img_url=post.img_url,
		body=post.body
	)
	if form.validate_on_submit():
		flash('Post successfully edited.')
		post.title = form.title.data
		post.subtitle = form.subtitle.data
		post.img_url = form.img_url.data
		post.body = form.body.data

		db.session.commit()

		return redirect(url_for("main_bp.post", post_id=post.id))

	return render_template("create_post.html", form=form, current_user=current_user)


@main_bp.route('/update-comment', methods=['POST'])
def update_comment():
	# Get the comment ID and new comment text from the request's JSON data
	data = request.get_json()
	comment_id = data.get('comment_id')
	comment_text = data.get('comment_text')
	print(post_id)

	# Update the comment in your database or wherever you store your comments
	comment = Comment.query.get(comment_id)
	comment.text = comment_text

	db.session.commit()

	# Return a JSON response indicating success
	return jsonify({'success': True})


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
