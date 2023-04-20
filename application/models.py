from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash


# User table for database
class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(
		db.Integer,
		primary_key=True,
	)
	email = db.Column(
		db.String(100),
		unique=True,
	)
	password = db.Column(
		db.String(500),
	)
	username = db.Column(
		db.String(50),
		unique=True,
	)
	created_on = db.Column(
		db.DateTime,
	)
	last_login = db.Column(
		db.DateTime,
	)
	posts = relationship(
		"BlogPost",
		back_populates="author",
	)
	comments = relationship(
		"Comment",
		back_populates="comment_author",
	)

	def set_password(self, password):
		"""Create hashed password."""
		self.password = generate_password_hash(
			password,
			method='pbkdf2:sha256',
			salt_length=8
		)

	def check_password(self, password):
		"""Check hashed password."""
		return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)


# Configure Blog Post Table
class BlogPost(db.Model):
	__tablename__ = "blog_posts"
	id = db.Column(
		db.Integer,
		primary_key=True,
	)
	author_id = db.Column(
		db.Integer,
		db.ForeignKey("users.id"),
	)
	author = relationship(
		"User",
		back_populates="posts",
	)
	title = db.Column(
		db.String(100),
		unique=True,
		nullable=False,
	)
	subtitle = db.Column(
		db.String(100),
		nullable=True,
	)
	created_on = db.Column(
		db.DateTime,
	)
	body = db.Column(
		db.Text,
		nullable=False,
	)
	img_url = db.Column(
		db.String(250),
		nullable=True,
	)
	comments = relationship(
		"Comment",
		back_populates="parent_post",
	)

	def __repr__(self):
		return '<BlogPost {}>'.format(self.title)


# Configure Comment Table
class Comment(db.Model):
	__tablename__ = "comments"
	id = db.Column(
		db.Integer,
		primary_key=True,
	)
	post_id = db.Column(
		db.Integer,
		db.ForeignKey("blog_posts.id"),
		unique=False,
	)
	author_id = db.Column(
		db.Integer,
		db.ForeignKey("users.id"),
	)
	parent_post = relationship(
		"BlogPost",
		back_populates="comments",
	)
	comment_author = relationship(
		"User",
		back_populates="comments",
	)
	text = db.Column(
		db.Text,
		nullable=False,
	)
	created_on = db.Column(
		db.DateTime,
		index=False,
		unique=False,
		nullable=False,
	)

	def __repr__(self):
		return '<Comment {}>'.format(self.text)
