from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_assets import Environment
import openai
from os import environ, path
from dotenv import load_dotenv
from flask_ckeditor import CKEditor


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

# Globally accessible libraries
db = SQLAlchemy()
bootstrap = Bootstrap5()
login_manager = LoginManager()
ckeditor = CKEditor()

openai.api_key = environ.get('OPENAI_API_KEY')


def init_app():
	"""Initialize the core application."""
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object('config.DevConfig')

	# Initialize Plugins
	db.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	ckeditor.init_app(app)
	assets = Environment(app)


	with app.app_context():
		# Include our Routes
		from . import routes, auth
		from .assets import compile_static_assets

		# Import blueprints
		app.register_blueprint(routes.main_bp)
		app.register_blueprint(auth.auth_bp)

		# Compile static assets
		compile_static_assets(assets)

		# Create sql tables for our data models
		db.create_all()

		return app
