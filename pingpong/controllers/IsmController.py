from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask_login import current_user
from flask_login import login_required
from pingpong.forms.IsmForm import IsmForm
from pingpong.services.IsmService import IsmService

ismController = Blueprint("ismController", __name__)

ismService = IsmService()
ismForm = IsmForm()

@ismController.route("/isms", methods = ["GET"])
def isms():
	if current_user.is_authenticated:
		isms = ismService.select()
	else:
		isms = ismService.selectApproved()

	return render_template("isms/index.html", isms = isms)

@ismController.route("/isms.json", methods = ["GET"])
def isms_json():
	isms = ismService.select()
	return Response(ismService.serialize(isms), status = 200, mimetype = "application/json")

@ismController.route("/isms/new", methods = ["GET"])
def isms_new():
	ism = ismService.new()
	return render_template("isms/new.html", ism = ism)

@ismController.route("/isms", methods = ["POST"])
def isms_create():
	hasErrors = ismForm.validate(request.form)

	if hasErrors:
		ism = ismService.new()
		ismForm.load(ism, request.form)
		return render_template("isms/new.html", ism = ism), 400
	else:
		ism = ismService.create(request.form)
		flash("Ism '{}' has been successfully created.".format(ism.saying), "success")
		return redirect("/isms")

@ismController.route("/isms/<int:id>/edit", methods = ["GET"])
def isms_edit(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	return render_template("isms/edit.html", ism = ism)

@ismController.route("/isms/<int:id>", methods = ["POST"])
def isms_update(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	hasErrors = ismForm.validate(request.form)

	if hasErrors:
		ismForm.load(ism, request.form)
		return render_template("isms/edit.html", ism = ism), 400

	else:
		ism = ismService.update(id, request.form)
		flash("Ism '{}' has been successfully updated.".format(ism.saying), "success")
		return redirect("/isms")

@ismController.route("/isms/<int:id>/approve", methods = ["POST"])
@login_required
def isms_enable(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ismService.approve(ism)

	flash("Ism '{}' has been approved.".format(ism.saying), "success")

	return redirect("/isms")

@ismController.route("/isms/<int:id>/reject", methods = ["POST"])
@login_required
def isms_disable(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ismService.reject(ism)

	flash("Ism '{}' has been rejected.".format(ism.saying), "success")

	return redirect("/isms")

@ismController.route("/isms/<int:id>/delete", methods = ["POST"])
@login_required
def isms_delete(id):
	ism = ismService.selectById(id)

	if ism == None:
		abort(404)

	ism, success = ismService.delete(ism)

	if success:
		flash("Ism '{}' has been successfully deleted.".format(ism.saying), "success")
	else:
		flash("Ism '{}' could not be deleted.".format(ism.saying), "warning")

	return redirect("/isms")
