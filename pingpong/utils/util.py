from datetime import datetime
from flask import current_app as app
from flask import request
from flask import request
from flask import send_from_directory
import hashlib
import os
import random
import uuid

def formatTime(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)

def param(name, default = None, paramType = None):
	value = request.args.get(name)

	if value == None:
		value = default

	if value != None and paramType != None:
		try:
			if paramType == "int":
				value = int(value)
			elif paramType == "str":
				value = str(value)
		except:
			return None

	return value

def paramForm(name, default = None, paramType = None):
	value = None

	if name in request.form:
		value = request.form[name]

	if value == None:
		value = default

	if value != None and paramType != None:
		if paramType == "int":
			value = int(value)
		elif paramType == "str":
			value = str(value)
		elif paramType == "bool":
			value = value in ("True", "true")

	return value

def jsonSerial(obj):
	if isinstance(obj, datetime):
		return str(obj)

def shuffle(ary):
	if len(ary) < 2:
		return ary

	newAry = ary[:]
	random.shuffle(newAry)

	if ary == newAry:
		return shuffle(ary)

	return newAry

def hash(string):
	return hashlib.sha224(string).hexdigest()

def hasConfig(param):
	if param not in app.config:
		return False

	if isinstance(app.config[param], bool):
		return True

	if len(app.config[param]) == 0:
		return False

	return True

def date(value):
	if value == None:
		return None

	return str(value)

def generateUUID():
	return str(uuid.uuid4())

def uploadAvatar(player):
	if "avatar" in request.files:
		avatar = request.files["avatar"]

		if len(avatar.filename) != 0:
			extension = avatar.filename.split(".")[-1]
			name = "{}.{}".format(generateUUID(), extension)
			avatar.save("{}/storage/avatars/{}".format(app.root_path, name))
			deleteAvatar(player.avatar)

			return True, name, extension

	return False, None, None

def deleteAvatar(avatar):
	if avatar == None:
		return

	avatarPath = "{}/storage/avatars/{}".format(app.root_path, avatar)

	if os.path.isfile(avatarPath):
		os.remove(avatarPath)

def avatar(player):
	return send_from_directory("{}/storage/avatars/".format(app.root_path), player.avatar, mimetype = "image/{}".format(player.extension))
