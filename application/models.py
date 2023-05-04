from . import db, whooshee
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5



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

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
			digest,
			size,
		)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

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

	def __repr__(self):
		return '<User {}>'.format(self.username)


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
