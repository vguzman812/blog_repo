from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address.")
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
