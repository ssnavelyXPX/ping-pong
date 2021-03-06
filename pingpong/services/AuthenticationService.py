from flask import current_app as app
from flask import request
from pingpong.models.AdminModel import AdminModel
from pingpong.utils import util

class AuthenticationService():

	def authenticate(self, form):
		app.logger.info("Authenticating Administrator")

		if "username" not in form:
			app.logger.info("Username field does not exist")
			return False

		if "password" not in form:
			app.logger.info("Password field does not exist")
			return False

		username = form["username"]
		password = form["password"]

		passwordHash = util.hash(password)

		if passwordHash != app.config["ADMIN_PASSWORD"]:
			app.logger.info("Invalid Password")
			return False

		if username != app.config["ADMIN_USERNAME"]:
			app.logger.info("Invalid Username")
			return False

		return True

	def admin(self):
		return AdminModel()
