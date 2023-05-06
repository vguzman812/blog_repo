from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class EditProfileForm(FlaskForm):
	new_username = StringField("Username", validators=[
	])
	new_email = StringField("Email", validators=[
		Email(message="Not a valid email address.")
	])
	new_password = PasswordField("Password", validators=[
	])
	confirm_password = PasswordField("Confirm Password", validators=[
		EqualTo('new_password', message="Passwords must match.")
	])
	about_me = TextAreaField('About me', validators=[
		Length(min=0, max=280, message='About me may be 280 characters maximum.'),
	])
	submit = SubmitField("Change all my stuff!")


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
	username = StringField("Username", validators=[
		DataRequired(),
		Length(min=4, max=50, message='Username must be between 4 and 50 characters.')
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address."),
		Length(max=100, message='Email must not be longer than 100 characters.')
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
