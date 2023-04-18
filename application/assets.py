"""
Compile static asset bundles.
Takes js or style sheets from src dir, compresses the files, and replicates the compressed files as output name
"""
from flask_assets import Bundle
import os


def compile_main_assets(assets):
	# tells assets where root dir is for compiling
	assets.load_path = [
		os.path.join(os.path.dirname(__file__), 'static'),
	]
	scss_filters = 'scss, cssmin'
	js_filters = 'jsmin'
	bundles = {
		'css_bootstrap': Bundle(
			'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
			filters='cssmin',
			output='dist/css/bootstrap.css'
		),
		'css_main': Bundle(
			'src/scss/main.scss',
			filters=scss_filters,
			output='dist/css/main.css',
		),
		'css_dashboard': Bundle(
			'src/scss/dashboard.scss',
			filters=scss_filters,
			output='dist/css/dashboard.css',
		),
		'css_register': Bundle(
			'src/scss/register.scss',
			filters=scss_filters,
			output='dist/css/register.css',
		),
		'css_login': Bundle(
			'src/scss/login.scss',
			filters=scss_filters,
			output='dist/css/login.css',
		),
		'css_index': Bundle(
			'src/scss/index.scss',
			filters=scss_filters,
			output='dist/css/index.css',
		),
		'css_post': Bundle(
			'src/scss/post.scss',
			filters=scss_filters,
			output='dist/css/post.css',
		),
		'js_bootstrap': Bundle(
			'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
			filters=js_filters,
			output='dist/js/bootstrap.js',
		),
		'js_dashboard': Bundle(
			'src/js/dashboard.js',
			filters=js_filters,
			output='dist/js/dashboard.js'
		),
		'js_register': Bundle(
			'src/js/register.js',
			filters=js_filters,
			output='dist/js/register.js'
		),
		'js_nav': Bundle(
			'src/js/nav.js',
			filters=js_filters,
			output='dist/js/nav.js'
		),
	}

	assets.register(bundles)

	for bundle in bundles:
		assets.register(bundle, bundles[bundle])
		bundles[bundle].build()


def compile_static_assets(assets):
	"""Compile all asset bundles."""
	compile_main_assets(assets)
# compile_auth_assets(assets)
