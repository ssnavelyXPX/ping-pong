from pingpong.forms.Form import Form
from pingpong.services.PlayerService import PlayerService

playerService = PlayerService()

class PlayerForm(Form):

	def fields(self):
		return [{
			"name": "name",
			"label": "Name",
			"required": True,
			"type": "string",
			"maxlength": 257
		}]

	def load(self, player, form):
		if "name" in form:
			player.name = form["name"]

	def validate(self, id, officeId, form):
		Form.validate(self, form)

		if not self.hasErrors:

			if id == None:
				players = playerService.selectByName(officeId, form["name"])
				self.foundNameError(players, form)
			else:
				players = playerService.selectByNameExcludingPlayer(officeId, id, form["name"])
				self.foundNameError(players, form)

			self.flash()

		return self.hasErrors

	def foundNameError(self, players, form):
		if players.count() > 0:
			message = "The name '{}' is already taken. Please specify a unique name.".format(form["name"])
			self.hasErrors = True
			self.errors.append(self.error({
				"name": "name",
				"label": "Name"
			}, message))
