"""Route declaration."""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime as dt
from application.models import db, User, BlogPost, Comment
from .forms import CommentForm, CreatePostForm, EmptyForm
from application.main import bp



@bp.route('/dashboard/user/<int:user_id>', methods=['GET'])
@login_required
def dashboard(user_id):
	form = EmptyForm()
	"""Logged in user dashboard."""
	user = User.query.get_or_404(user_id)
	user_posts = BlogPost.query.filter_by(author_id=user_id).all()
	return render_template(
		'dashboard.html',
		user_posts=user_posts,
		user=user,
		form=form,
	)


@bp.route('/dashboard/user/<int:user_id>/comments', methods=['GET'])
@login_required
def dashboard_comments(user_id):
	"""Logged in user dashboard."""
	form = EmptyForm()
	user = User.query.get_or_404(user_id)
	all_posts = BlogPost.query.all()
	user_comments = Comment.query.filter_by(author_id=user_id).all()
	return render_template(
		'dashboard.html',
		user_comments=user_comments,
		all_posts=all_posts,
		user=user,
		form=form,
	)


@bp.route('/dashboard/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def dashboard_edit(user_id):
	"""
	Edit page for user info. User can edit username, email, password, and about me.
	:param user_id:
	:return:
	"""
	return render_template(
		'dashboard.html',
	)


@bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			flash('User {} not found.'.format(user_id))
			return redirect(url_for('main.index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for('main.dashboard', user_id=user_id))
		current_user.follow(user)
		db.session.commit()
		flash('You are following user {}!'.format(user_id))
		return redirect(url_for('main.dashboard', user_id=user_id))
	else:
		return redirect(url_for('main.index'))


@bp.route('/dashboard/user/<int:user_id>/following', methods=['GET'])
@login_required
def following(user_id):
	"""Logged in user dashboard."""
	form = EmptyForm()
	user = User.query.get_or_404(user_id)
	followed_users = user.followed_users().all()
	print(followed_users)

	return render_template(
		'dashboard.html',
		user=user,
		followed_users=followed_users,
		form=form,
	)


@bp.route('/dashboard/user/<int:user_id>/followers', methods=['GET'])
@login_required
def followers(user_id):
	"""Logged in user dashboard."""
	form = EmptyForm()
	user = User.query.get_or_404(user_id)
	following_users = user.following_users().all()
	print(following_users)

	return render_template(
		'dashboard.html',
		user=user,
		followers=following_users,
		form=form,
	)


@bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			flash('User {} not found.'.format(user_id))
			return redirect(url_for('main.index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for('main.dashboard', user_id=user_id))
		current_user.unfollow(user)
		db.session.commit()
		flash('You are not following {}.'.format(user_id))
		return redirect(url_for('main.dashboard', user_id=user_id))
	else:
		return redirect(url_for('main.index'))


@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = dt.utcnow()
		db.session.commit()


# home page
@bp.route('/')
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


@bp.route("/post/<int:post_id>", methods=["GET", "POST"])
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
			return redirect(url_for("main.post", post_id=post_id))

		new_comment = Comment(
			text=form.comment_text.data,
			author_id=current_user.id,
			post_id=form.post_id.data,
			created_on=dt.utcnow(),
		)
		db.session.add(new_comment)
		db.session.commit()
		return redirect(url_for('main.post', post_id=post_id))

	return render_template(
		"post.html",
		post=requested_post,
		author=author,
		form=form,
		current_user=current_user,
	)


@bp.route('/create_post', methods=["GET", "POST"])
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
			created_on=dt.utcnow(),
		)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for("main.post", post_id=new_post.id))
	return render_template(
		"create_post.html",
		form=form,
		current_user=current_user,
	)


@bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
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

		return redirect(url_for("main.post", post_id=post.id))

	return render_template("create_post.html", form=form, current_user=current_user)


@bp.route('/delete_comment/<int:comment_id>', methods=['GET'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if not comment.author_id == current_user.id:
		return redirect(url_for('main.post', post_id=comment.post_id))
	else:
		db.session.delete(comment)
		db.session.commit()
	return redirect(url_for('main.post', post_id=comment.post_id))
