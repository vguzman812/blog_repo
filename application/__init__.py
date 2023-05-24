from dotenv import load_dotenv
from flask import Flask
from flask_assets import Environment
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from logging.handlers import SMTPHandler, RotatingFileHandler
from os import path
from sqlalchemy import MetaData

import config
import logging
import os


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

# Needed for Flask-Migrate / SQLite constraint naming discrepancies.
metadata = MetaData(
	naming_convention={
		"ix": 'ix_%(column_0_label)s',
		"uq": "uq_%(table_name)s_%(column_0_name)s",
		"ck": "ck_%(table_name)s_%(constraint_name)s",
		"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
		"pk": "pk_%(table_name)s"
	}
)

# Globally accessible libraries
bootstrap = Bootstrap5()
ckeditor = CKEditor()
db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
moment = Moment()
whooshee = Whooshee()


def init_app(config_class=config.ProdConfig):
	"""Initialize the core application."""
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object(config_class)

	# Initialize Plugins
	assets = Environment(app)
	bootstrap.init_app(app)
	ckeditor.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	whooshee.init_app(app)

	with app.app_context():
		# Include our Routes
		from . import main, auth, errors
		from .assets import compile_static_assets

		# Import blueprints
		app.register_blueprint(auth.bp)
		app.register_blueprint(errors.bp)
		app.register_blueprint(main.bp)

		# Compile static assets
		compile_static_assets(assets)

		# Create sql tables for our data models
		db.create_all()

		migrate.init_app(app, db, render_as_batch=True)

		#Initialize logger if in production
		if not app.debug and not app.testing:
			if app.config['LOG_TO_STDOUT']:
				stream_handler = logging.StreamHandler()
				stream_handler.setLevel(logging.INFO)
				app.logger.addHandler(stream_handler)
			else:
				if not path.exists('logs'):
					os.mkdir('logs')
				file_handler = RotatingFileHandler('logs/ideagenie.log', maxBytes=10240, backupCount=10)
				file_handler.setFormatter(logging.Formatter(
					'%(asctime)s %(levelname)s: %(message)s '
					'[in %(pathname)s:%(lineno)d]'))
				file_handler.setLevel(logging.INFO)
				app.logger.addHandler(file_handler)

			app.logger.setLevel(logging.INFO)
			app.logger.info('IdeaGenie startup')
		return app
