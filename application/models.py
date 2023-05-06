from . import db, whooshee
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from hashlib import md5
import jwt
from sqlalchemy.orm import relationship
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

# Followers association Table
followers = db.Table(
	'followers',
	db.Column(
		'follower_id',
		db.Integer,
		db.ForeignKey('users.id')
	),
	db.Column(
		'followed_id',
		db.Integer,
		db.ForeignKey('users.id')
	),
)


# Configure Blog Post Table
@whooshee.register_model('title', 'subtitle', 'body')
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
		default=datetime.utcnow,
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
		backref="parent_post",
		lazy='dynamic',
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
	text = db.Column(
		db.Text,
		nullable=False,
	)
	created_on = db.Column(
		db.DateTime,
		default=datetime.utcnow,
	)

	def __repr__(self):
		return '<Comment {}>'.format(self.text)


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
		db.String(),
	)
	username = db.Column(
		db.String(50),
		unique=True,
	)
	created_on = db.Column(
		db.DateTime,
		default=datetime.utcnow
	)
	last_seen = db.Column(
		db.DateTime,
	)
	about_me = db.Column(
		db.String(280),
	)
	verified = db.Column(
		db.Boolean,
	)
	posts = relationship(
		"BlogPost",
		backref="author",
		lazy='dynamic',
	)
	comments = relationship(
		"Comment",
		backref="comment_author",
		lazy='dynamic',
	)

	followed = relationship(
		'User',
		secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'),
		lazy='dynamic',
	)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
			digest,
			size,
		)

	def check_password(self, password):
		"""Check hashed password."""
		return check_password_hash(self.password, password)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def followed_users(self):
		return User.query.join(
			followers,
			(followers.c.followed_id == User.id)
		).filter(
			followers.c.follower_id == self.id
		)

	def following_users(self):
		return User.query.join(
			followers,
			(followers.c.follower_id == User.id)
		).filter(
			followers.c.followed_id == self.id
		)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{
				'reset_password': self.id,
				'exp': time() + expires_in
			},
			current_app.config['SECRET_KEY'],
			algorithm='HS256')

	def get_verification_token(self, expires_in=600):
		return jwt.encode(
			{
				'verify_email': self.id,
				'exp': time() + expires_in
			},
			current_app.config['SECRET_KEY'],
			algorithm='HS256')

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def set_password(self, password):
		"""Create hashed password."""
		self.password = generate_password_hash(
			password,
			method='pbkdf2:sha256',
			salt_length=8
		)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(
				token,
				current_app.config['SECRET_KEY'],
				algorithms=['HS256'],
			)['reset_password']
		except:
			return
		return User.query.get(id)
	@staticmethod
	def verify_verification_token(token):
		try:
			id = jwt.decode(
				token,
				current_app.config['SECRET_KEY'],
				algorithms=['HS256'],
			)['verify_email']
		except:
			return
		return User.query.get(id)

	def __repr__(self):
		return '<User {}>'.format(self.username)
