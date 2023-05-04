from application import whooshee
from flask import current_app


def reindex_search():
	with current_app.app_context():
		whooshee.reindex()
