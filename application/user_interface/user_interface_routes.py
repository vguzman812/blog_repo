from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
user_interface_bp = Blueprint(
	'user_interface_bp', __name__,
	template_folder='templates',
	static_folder='static'
)


@user_interface_bp.route('/dashboard', methods=['GET'])
def dashboard():
	"""Logged in user dashboard."""
	return render_template(
		'dashboard.html',
	)
