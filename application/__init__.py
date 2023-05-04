from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_assets import Environment
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy import MetaData
from os import environ, path
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
from flask_whooshee import Whooshee

import config

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
db = SQLAlchemy(metadata=metadata)
bootstrap = Bootstrap5()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()
ckeditor = CKEditor()
whooshee = Whooshee()


def init_app(config_class=config.DevConfig):
	"""Initialize the core application."""
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object(config_class)

	# Initialize Plugins
	db.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	moment.init_app(app)
	ckeditor.init_app(app)
	whooshee.init_app(app)
	assets = Environment(app)

	with app.app_context():
		# Include our Routes
		from . import main, auth, errors
		from .assets import compile_static_assets

		# Import blueprints
		app.register_blueprint(main.bp)
		app.register_blueprint(auth.bp)
		app.register_blueprint(errors.bp)

		# Compile static assets
		compile_static_assets(assets)

		# Create sql tables for our data models
		db.create_all()

		migrate.init_app(app, db, render_as_batch=True)

		return app
