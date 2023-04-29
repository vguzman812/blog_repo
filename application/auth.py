from flask import Flask, render_template, redirect, url_for, flash, abort, make_response
from flask import Blueprint, request, session
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, RegisterForm
from .models import db, User, BlogPost, Comment
from . import login_manager
from functools import wraps
from datetime import datetime

# Blueprint Configuration
auth_bp = Blueprint(
	'auth_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


# function that gives administrative privileges when decorating
def admin_only(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.id != 1:
			return abort(403)
		return f(*args, **kwargs)

	return decorated_function


@login_manager.user_loader
def load_user(user_id):
	"""Check if user is logged-in on every page load."""
	if user_id is not None:
		return User.query.get(user_id)
	return None


@login_manager.unauthorized_handler
def unauthorized():
	"""Redirect unauthorized users to Login page."""
	flash('You must be logged in to view that page.')
	return redirect(url_for('auth_bp.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
	"""
	User sign-up page.

	GET requests serve sign-up page.
	POST requests validate form & user creation.
	"""
	# Bypass if user is logged in
	if current_user.is_authenticated:
		flash('Log out first to register a new account.')
		return redirect(url_for('auth_bp.dashboard', user_id=current_user.id))

	form = RegisterForm()
	if form.validate_on_submit():
		existing_user_by_email = User.query.filter_by(email=form.email.data).first()
		existing_user_by_username = User.query.filter_by(username=form.username.data).first()
		if existing_user_by_email:
			flash('A user already exists with that email address.')
		if existing_user_by_username:
			flash('A user already exists with that username.')
		if existing_user_by_email is None and existing_user_by_username is None:
			user = User(
				username=form.username.data,
				email=form.email.data,
				created_on=datetime.now(),
				last_login=datetime.now(),
			)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()  # Create new user
			login_user(user)  # Log in as newly created user
			flash('Successfully Registered!')
			return redirect(url_for('auth_bp.dashboard', user_id=current_user.id))
	return render_template(
		'register.html',
		form=form,
	)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Log-in page for registered users.

	GET requests serve Log-in page.
	POST requests validate and redirect user to dashboard.
	"""
	# Bypass if user is logged in
	if current_user.is_authenticated:
		flash('You are already logged in.')
		return redirect(url_for('auth_bp.dashboard', user_id=current_user.id))

	form = LoginForm()
	# Validate login attempt
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user and user.check_password(password=form.password.data):
			login_user(user)
			user.last_login = datetime.utcnow()
			db.session.commit()
			return redirect(url_for('auth_bp.dashboard', user_id=current_user.id))
		flash('Invalid email/password combination')
		return redirect(url_for('auth_bp.login'))
	return render_template(
		'login.html',
		form=form,
	)


@auth_bp.route('/dashboard/user/<int:user_id>', methods=['GET'])
@login_required
def dashboard(user_id):
	"""Logged in user dashboard."""
	user_posts = BlogPost.query.filter_by(author_id=user_id).all()
	return render_template(
		'dashboard.html',
		user_posts=user_posts,
	)


@auth_bp.route('/dashboard/user/<int:user_id>/comments', methods=['GET'])
@login_required
def dashboard_comments(user_id):
	"""Logged in user dashboard."""
	all_posts = BlogPost.query.all()
	user_comments = Comment.query.filter_by(author_id=user_id).all()
	return render_template(
		'dashboard.html',
		user_comments=user_comments,
		all_posts=all_posts,
	)
