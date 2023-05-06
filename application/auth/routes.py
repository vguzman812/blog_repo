from application import login_manager
from application.models import db, User
from application.auth import bp
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, RegisterForm, EditProfileForm
from werkzeug.urls import url_parse


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
	return redirect(url_for('auth.login'))


@bp.route('/dashboard/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
	"""
	Edit page for user info. User can edit username, email, password, and about me.
	"""
	user = User.query.get_or_404(user_id)
	if current_user.id != user.id:
		return redirect(url_for('main.dashboard', user_id=current_user.id))
	form = EditProfileForm(
		new_username=user.username,
		new_email=user.email,
		about_me=user.about_me,
	)
	if form.validate_on_submit():
		# Check if the new username and email are different from the current ones
		if (form.new_username.data != user.username and
				User.query.filter_by(username=form.new_username.data).first()):
			flash('Username is already taken.')
			return redirect(url_for('auth.edit_user', user_id=user_id))

		if (form.new_email.data != user.email and
				User.query.filter_by(email=form.new_email.data).first()):
			flash('Email is already taken.')
			return redirect(url_for('auth.edit_user', user_id=user_id))

		# Update the user's data if all validation checks pass
		if form.new_username.data != user.username:
			user.username = form.new_username.data
		if form.new_email.data != user.email:
			user.email = form.new_email.data
		if form.new_password.data:
			user.set_password(form.new_password.data)
		if form.about_me.data != user.about_me:
			user.about_me = form.about_me.data

		db.session.commit()

		flash('Profile successfully edited.')
		return redirect(url_for("main.dashboard", user_id=current_user.id))

	return render_template(
		'auth/edit_profile.html',
		form=form,
		user=current_user,
	)


@bp.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Log-in page for registered users.

	GET requests serve Log-in page.
	POST requests validate and redirect user to dashboard.
	"""
	# Bypass if user is logged in
	if current_user.is_authenticated:
		flash('You are already logged in.')
		return redirect(url_for('main.dashboard', user_id=current_user.id))
	form = LoginForm()
	# Validate login attempt
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user and user.check_password(password=form.password.data):
			login_user(user)
			user.last_seen = datetime.utcnow()
			db.session.commit()
			next_page = request.args.get('next')
			if not next_page or url_parse(next_page).netloc != '':
				next_page = url_for('main.index')
			return redirect(next_page)
		flash('Invalid email/password combination')
		return redirect(url_for('auth.login'))
	return render_template(
		'auth/login.html',
		form=form,
	)


@bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
	"""
	User sign-up page.

	GET requests serve sign-up page.
	POST requests validate form & user creation.
	"""
	# Bypass if user is logged in
	if current_user.is_authenticated:
		flash('Log out first to register a new account.')
		return redirect(url_for('main.index'))

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
				last_seen=datetime.now(),
			)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()  # Create new user
			login_user(user)  # Log in as newly created user
			flash('Successfully Registered!')
			return redirect(url_for('main.dashboard', user_id=current_user.id))
	return render_template(
		'auth/register.html',
		form=form,
	)
