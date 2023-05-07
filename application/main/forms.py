from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length


class CommentForm(FlaskForm):
	post_id = HiddenField()
	comment_text = TextAreaField("Comment", validators=[
		DataRequired(),
	])
	submit = SubmitField("Submit Comment")


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


# WTForms
class CreatePostForm(FlaskForm):
	title = StringField("Blog Post Title", validators=[
		DataRequired(),
		Length(min=5, max=100, message='Title must be between 5-100 characters'),
	])
	subtitle = StringField("Subtitle", validators=[
		DataRequired(),
		Length(min=5, max=100, message='Title must be between 5-100 characters'),
	])
	img_url = StringField("Blog Image URL", validators=[
		DataRequired(),
		URL(),
		Length(max=250, message='URL must be less than 250 characters long. Choose a different URL.')
	])
	body = CKEditorField("Blog Content", validators=[
		DataRequired(),
	])
	submit = SubmitField("Submit Post")


class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')


class UploadForm(FlaskForm):
	upload = FileField('image', validators=[
		FileRequired(),
		FileAllowed(['jpg', 'png'], 'Images only!')
	])
