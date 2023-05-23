from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from ..models import User


class EditProfileForm(FlaskForm):
	new_username = StringField('Username', validators=[
		DataRequired(),
		Length(1, 64),
		Regexp(
			'^[A-Za-z][A-Za-z0-9_.]*$',
			0,
			'Usernames must have only letters, numbers, dots or underscores'),
	])
	new_email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address."),
		Length(max=64, message='Email must not be longer than 64 characters.')
	])
	new_password = PasswordField("Password", validators=[
		Length(min=6, message="Minimum length is 6 characters"),
	])
	confirm_password = PasswordField("Confirm Password", validators=[
		EqualTo('password', message="Passwords must match.")
	])
	about_me = TextAreaField('About me', validators=[
		Length(min=0, max=280, message='About me may be 280 characters maximum.'),
	])
	submit = SubmitField("Change all my stuff!")

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')



class LoginForm(FlaskForm):
	email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address")
	])
	password = PasswordField("Password", validators=[
		DataRequired(),
	])
	submit = SubmitField("Let Me In!")


class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(),
		Length(1, 64),
		Regexp(
			'^[A-Za-z][A-Za-z0-9_.]*$',
			0,
			'Usernames must have only letters, numbers, dots or underscores'),
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address."),
		Length(max=64, message='Email must not be longer than 64 characters.')
	])
	password = PasswordField("Password", validators=[
		DataRequired(),
		Length(min=6, message="Minimum length is 6 characters"),
	])
	confirm_password = PasswordField("Confirm Password", validators=[
		DataRequired(),
		EqualTo('password', message="Passwords must match.")
	])
	submit = SubmitField("Sign Me Up!")

	def validate_email(self, field):
		if field.data != self.user.email and \
				User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('New Password', validators=[
		DataRequired(),
	])
	password2 = PasswordField('Confirm New Password', validators=[
		DataRequired(),
		EqualTo('password'),
	])
	submit = SubmitField('Reset my password')


class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[
		DataRequired(),
		Email(),
	])
	submit = SubmitField('Request password reset')
