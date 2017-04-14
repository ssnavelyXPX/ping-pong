from MatchType import MatchType
from pingpong.utils import notifications
import random

class Doubles(MatchType):

	def __init__(self):
		MatchType.__init__(self, "Doubles", "doubles", "matches/doubles.html", 21, 4, 2)

	def matchData(self, match):
		game = match.games[match.game - 1]

		data = {
			"matchId": match.id,
			"matchType": self.matchType,
			"playTo": match.playTo,
			"numOfGames": match.numOfGames,
			"game": match.game,
			"template": self.matchTemplate,
			"complete": match.complete == 1,
			"teams": {
				"north": self.newTeam(),
				"south": self.newTeam()
			},
			"players": {},
			"points": 0
		}

		for color in self.colors:
			data["players"][color] = self.newPlayer(getattr(game, color))

		data["points"] = self.setTeamData(match, data["players"], data["teams"])
		self.determineWinner(match, data["teams"])
		self.determineServe(data["points"], data["players"])

		return data

	def newTeam(self):
		return {
			"teamId": None,
			"points": 0,
			"winner": False,
			"players": [],
			"games": []
		}

	def newPlayer(self, playerId):
		return {
			"playerId": playerId,
			"playerName": None,
			"serving": False
		}

	def setTeamData(self, match, players, teams):
		for team in match.teams:

			points = self.scoreService.getScore(match.id, team.id, match.game)

			for player in team.players:
				if players["green"]["playerId"] == player.id:
					color = "green"
					teams["north"]["teamId"] = team.id
					teams["north"]["points"] = points
					teams["north"]["players"].append(player.name)
					teams["north"]["winner"] = (team.win == 1)

				elif players["yellow"]["playerId"] == player.id:
					color = "yellow"
					teams["south"]["teamId"] = team.id
					teams["south"]["points"] = points
					teams["south"]["players"].append(player.name)
					teams["south"]["winner"] = (team.win == 1)

				elif players["blue"]["playerId"] == player.id:
					color = "blue"
					teams["south"]["players"].append(player.name)

				elif players["red"]["playerId"] == player.id:
					color = "red"
					teams["north"]["players"].append(player.name)

				players[color]["playerName"] = player.name
				players[color]["teamId"] = team.id

		return teams["north"]["points"] + teams["south"]["points"]

	def determineWinner(self, match, teams):
		for game in match.games:
			if game.winner == teams["north"]["teamId"]:
				winner = teams["north"]
				loser = teams["south"]
			else:
				loser = teams["north"]
				winner = teams["south"]

			winner["games"].append({
				"win": None if game.winner == None else True,
				"score": game.winnerScore
			})
			loser["games"].append({
				"win": None if game.winner == None else False,
				"score": game.loserScore
			})

	def determineServe(self, points, players):

		# green serves first and swaps after serving is complete
		if (points - 5) % 20 < 10:
			green = players["green"]
			red = players["red"]
			players["green"] = red
			players["red"] = green

		# blue serves second and swaps after serving is complete
		if (points) % 20 >= 10:
			yellow = players["yellow"]
			blue = players["blue"]
			players["yellow"] = blue
			players["blue"] = yellow

		if points % 10 < 5:
			players["green"]["serving"] = True
		else:
			players["blue"]["serving"] = True

	def determineGameWinner(self, match):
		data = self.matchData(match)
		north = data["teams"]["north"]
		south = data["teams"]["south"]

		northWin = north["points"] >= data["playTo"] and north["points"] >= south["points"] + 2
		southWin = south["points"] >= data["playTo"] and south["points"] >= north["points"] + 2

		if northWin or southWin:
			if northWin:
				winner = north["teamId"]
				winnerScore = north["points"]
				loser = south["teamId"]
				loserScore = south["points"]
			elif southWin:
				winner = south["teamId"]
				winnerScore = south["points"]
				loser = north["teamId"]
				loserScore = north["points"]

			self.gameService.complete(data["matchId"], data["game"], winner, winnerScore, loser, loserScore)

			self.determineMatchWinner(match)

			if not match.complete and match.game < match.numOfGames:
				self.matchService.updateGame(match.id, match.game + 1)

	def createTeams(self, match, data, randomize):
		ids = map(int, data)

		if randomize:
			random.shuffle(ids)

		green = ids[0]
		yellow = ids[1]
		blue = ids[2]
		red = ids[3]

		team1 = self.teamService.createTwoPlayer(match.id, green, red)
		team2 = self.teamService.createTwoPlayer(match.id, yellow, blue)

		for i in range(0, match.numOfGames):

			# Game 1
			# B  A
			# C  D
			if i % 4 == 0:
				a = green
				b = yellow
				c = blue
				d = red

			# Game 2
			# A  B
			# D  C
			elif i % 4 == 1:
				a = yellow
				b = green
				c = red
				d = blue

			# Game 3
			# C  D
			# B  A
			elif i % 4 == 2:
				a = red
				b = blue
				c = yellow
				d = green

			# Game 4
			# D  C
			# A  B
			elif i % 4 == 3:
				a = blue
				b = red
				c = green
				d = yellow

			self.gameService.create(match.id, i + 1, a, b, c, d)

	def score(self, match, button):
		data = self.matchData(match)

		if button == "green" or button == "red":
			teamId = data["teams"]["north"]["teamId"]
		elif button == "yellow" or button == "blue":
			teamId = data["teams"]["south"]["teamId"]

		self.scoreService.score(match.id, teamId, match.game)

		self.determineGameWinner(match)

		return self.matchData(match)

	def playAgain(self, match, numOfGames, randomize):
		game = match.games[0]
		playerIds = [game.green, game.yellow, game.blue, game.red]

		newMatch = self.matchService.create(self.matchType)
		newMatch.numOfGames = numOfGames
		newMatch.game = 1
		self.createTeams(newMatch, playerIds, randomize)
		self.matchService.play(newMatch)

		return newMatch

	def sendWinningMessage(self, match, winningTeam, winningSets, losingTeam, losingSets):
		winnerPlayer1 = winningTeam.players[0]
		winnerPlayer2 = winningTeam.players[1]
		losingPlayer1 = losingTeam.players[0]
		losingPlayer2 = losingTeam.players[1]

		message = "<b>{}</b> and <b>{}</b> have defeated {} and {}, {} - {}".format(winnerPlayer1.name, winnerPlayer2.name, losingPlayer1.name, losingPlayer2.name, winningSets, losingSets)

		winnerScores = "\n"
		loserScores = "\n"

		for game in match.games:
			if game.completedAt == None:
				continue

			if game.winner == winningTeam.id:
				winnerScores += "<b>{}</b>\t\t\t".format(game.winnerScore)
				loserScores += "{}\t\t\t".format(game.loserScore)
			else:
				winnerScores += "{}\t\t\t".format(game.loserScore)
				loserScores += "<b>{}</b>\t\t\t".format(game.winnerScore)

		message += winnerScores
		message += loserScores

		notifications.send(message)
