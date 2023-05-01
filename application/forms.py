from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, EqualTo, Length
from flask_ckeditor import CKEditorField


# WTForms
class CreatePostForm(FlaskForm):
	title = StringField("Blog Post Title", validators=[
		DataRequired(),
	])
	subtitle = StringField("Subtitle", validators=[
		DataRequired(),
	])
	img_url = StringField("Blog Image URL", validators=[
		DataRequired(), URL(),
	])
	body = CKEditorField("Blog Content", validators=[
		DataRequired(),
	])
	submit = SubmitField("Submit Post")


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


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address")
	])
	password = PasswordField("Password", validators=[
		DataRequired(),
	])
	submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
	post_id = HiddenField()
	comment_text = TextAreaField("Comment", validators=[
		DataRequired(),
	])
	submit = SubmitField("Submit Comment")


class UploadForm(FlaskForm):
	upload = FileField('image', validators=[
		FileRequired(),
		FileAllowed(['jpg', 'png'], 'Images only!')
	])


class ContactForm(FlaskForm):
	"""Contact form."""
	name = StringField('Name', validators=[
		DataRequired(),
	])
	email = StringField('Email', validators=[
		Email(message='Not a valid email address.'),
		DataRequired(),
	])
	body = CKEditorField('Message', validators=[
		DataRequired(),
		Length(min=4, message='Your message is too short.'),
	])
	submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
	new_username = StringField("Username", validators=[
		DataRequired(),
	])
	new_email = StringField("Email", validators=[
		DataRequired(),
		Email(message="Not a valid email address.")
	])
	new_password = PasswordField("Password", validators=[
		DataRequired(),
		Length(min=6, message="Minimum length is 6 characters"),
	])
	confirm_password = PasswordField("Confirm Password", validators=[
		DataRequired(),
		EqualTo('password', message="Passwords must match.")
	])
	about_me = TextAreaField('About me', validators=[
		Length(min=0, max=280),
	])
	submit = SubmitField("Sign Me Up!")


class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')
