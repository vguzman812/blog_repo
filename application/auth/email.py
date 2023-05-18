from flask import render_template, current_app
from application.email import send_email


def send_password_reset_email(user):
	token = user.get_reset_password_token()
	send_email(
		'[IdeaGenie] Reset Your Password',
		sender=current_app.config['MAIL_USERNAME'],
		recipients=[user.email],
		text_body=render_template(
			'auth/email/reset_password_email.txt',
			user=user,
			token=token,
		),
		html_body=render_template(
			'auth/email/reset_password_email.html',
			user=user,
			token=token,
		),
	)


def send_verification_email(user):
	token = user.get_verification_token()
	send_email(
		'[IdeaGenie] Verify Your Email',
		sender=current_app.config['MAIL_USERNAME'],
		recipients=[user.email],
		text_body=render_template(
			'auth/email/verify_email.txt',
			user=user,
			token=token,
		),
		html_body=render_template(
			'auth/email/verify_email.html',
			user=user,
			token=token,
		),
	)
