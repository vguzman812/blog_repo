from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_assets import Environment
from flask_migrate import Migrate
import openai
from sqlalchemy import MetaData
from os import environ, path
from dotenv import load_dotenv
from flask_ckeditor import CKEditor


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

		migrate.init_app(app, db, render_as_batch=True)

		return app
