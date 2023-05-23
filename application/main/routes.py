"""Route declaration."""
from .forms import CommentForm, CreatePostForm, EmptyForm
from application.main import bp
from application.models import db, User, BlogPost, Comment
from application.route_constants import INDEX_ROUTE, DASH_ROUTE, POST_ROUTE
from application.search import reindex_search
from datetime import datetime as dt
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user


# Update user last_seen column
@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = dt.utcnow()
		db.session.commit()


# Create Post Route
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
		existing_post_by_title = BlogPost.query.filter_by(title=form.title.data).first()
		if existing_post_by_title:
			flash('There is already a post with that title. Please change the title.')
		if existing_post_by_title is None:
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
			reindex_search()
			return redirect(url_for(POST_ROUTE, post_id=new_post.id))
	return render_template(
		"create_post.html",
		form=form,
		current_user=current_user,
	)


# Render user dashboard with posts
@bp.route('/dashboard/user/<int:user_id>', methods=['GET'])
@login_required
def dashboard(user_id):
	"""Logged in user dashboard."""
	form = EmptyForm()
	user = User.query.get_or_404(user_id)
	user_posts = BlogPost.query.filter_by(author_id=user_id).all()
	return render_template(
		'dashboard.html',
		user_posts=user_posts,
		user=user,
		form=form,
	)


# Render user dashboard with comments
@bp.route('/dashboard/user/<int:user_id>/comments', methods=['GET'])
@login_required
def dashboard_comments(user_id):
	"""Logged in user dashboard."""
	form = EmptyForm()
	user = User.query.get_or_404(user_id)
	all_posts = BlogPost.query.all()
	if current_user.id == user_id:
		user_comments = Comment.query.filter_by(author_id=user_id).all()
	else:
		user_comments = db.session.query(Comment, BlogPost). \
			join(BlogPost, Comment.post_id == BlogPost.id). \
			filter(Comment.author_id == user_id). \
			all()
	return render_template(
		'dashboard.html',
		user_comments=user_comments,
		all_posts=all_posts,
		user=user,
		form=form,
	)


# Render user edit_profile page


# Delete comment route
@bp.route('/delete_comment/<int:comment_id>', methods=['GET'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if comment.author_id != current_user.id:
		return redirect(url_for(POST_ROUTE, post_id=comment.post_id))
	else:
		db.session.delete(comment)
		db.session.commit()
		flash('Comment successfully deleted!')
	return redirect(url_for('main.dashboard_comments', user_id=current_user.id))


# Delete post route
@bp.route('/delete_post/<int:post_id>', methods=['GET'])
@login_required
def delete_post(post_id):
	blog_post = BlogPost.query.get_or_404(post_id)
	if blog_post.author_id != current_user.id:
		return redirect(url_for(POST_ROUTE, post_id=blog_post.post_id))
	else:
		db.session.delete(blog_post)
		db.session.commit()
		flash('Post successfully deleted')
	return redirect(url_for(DASH_ROUTE, user_id=current_user.id))


# Edit post route
@bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
	blog_post = BlogPost.query.get_or_404(post_id)
	form = CreatePostForm(
		title=blog_post.title,
		subtitle=blog_post.subtitle,
		img_url=blog_post.img_url,
		body=blog_post.body
	)
	if form.validate_on_submit():
		blog_post.title = form.title.data
		blog_post.subtitle = form.subtitle.data
		blog_post.img_url = form.img_url.data
		blog_post.body = form.body.data

		db.session.commit()
		reindex_search()
		flash('Post successfully edited.')
		return redirect(url_for(POST_ROUTE, post_id=blog_post.id))

	return render_template("create_post.html", form=form, current_user=current_user)


# Follow user route
@bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first()
		if user is None:
			flash('User {} not found.'.format(user_id))
			return redirect(url_for(INDEX_ROUTE))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for(DASH_ROUTE, user_id=user_id))
		current_user.follow(user)
		db.session.commit()
		flash('You are now following user {}!'.format(user_id))
		return redirect(url_for(DASH_ROUTE, user_id=user_id))
	else:
		return redirect(url_for(INDEX_ROUTE))


# Render user followers dashboard page
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


# Render user following dashboard page
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


# Render home page
@bp.route('/')
def index():
	reindex_search()
	posts = BlogPost.query.all()
	page = request.args.get('page', 1, type=int)
	pagination = BlogPost.query.order_by(BlogPost.created_on.desc()).paginate(page=page, per_page=6)

	return render_template(
		"index.html",
		current_user=current_user,
		pagination=pagination,
		all_posts=posts,
	)

@bp.route('/browse')
def browse():
	page = request.args.get('page', 1, type=int)
	pagination = BlogPost.query.order_by(BlogPost.created_on.desc()).paginate(page=page, per_page=6)

	return render_template(
		"browse.html",
		pagination=pagination,
	)

# Render specific post page
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
			return redirect(url_for(POST_ROUTE, post_id=post_id))

		new_comment = Comment(
			text=form.comment_text.data,
			author_id=current_user.id,
			post_id=form.post_id.data,
			created_on=dt.utcnow(),
		)
		db.session.add(new_comment)
		db.session.commit()
		return redirect(url_for(POST_ROUTE, post_id=post_id))

	return render_template(
		"post.html",
		post=requested_post,
		author=author,
		form=form,
		current_user=current_user,
	)


# Search bar route
@bp.route('/search/<keyword>')
def search(keyword):
	search_results = BlogPost.query.whooshee_search(keyword).all()
	results = [
		{
			"title": result.title,
			"subtitle": result.subtitle,
			"url": url_for(POST_ROUTE, post_id=result.id),
		} for result in search_results
	]
	return jsonify(results)


# Unfollow user route
@bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=user_id).first_or_404()
		if user is None:
			flash('User {} not found.'.format(user_id))
			return redirect(url_for(INDEX_ROUTE))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for(DASH_ROUTE, user_id=user_id))
		current_user.unfollow(user)
		db.session.commit()
		flash('You are no longer following {}.'.format(user_id))
		return redirect(url_for(DASH_ROUTE, user_id=user_id))
	else:
		return redirect(url_for(INDEX_ROUTE))
