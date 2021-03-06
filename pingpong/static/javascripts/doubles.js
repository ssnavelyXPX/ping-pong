$(function(){

	var doubles = $("#doubles");

	if(doubles.exists()){

		var matchId = doubles.data("matchid");
		var office = $("meta[name=office]").attr("content");
		var disconnected = false;

		var socket = io.connect(domain());
		socket.on("response-" + office, update);
		socket.on("smack-talk-" + office, smackTalk);
		socket.on("disconnect", function(){
			if(!disconnected){
				setTimeout(function(){
					location.reload();
				}, 500);
			}
		});
		$(window).on("beforeunload", function(){
			disconnected = true;
			socket.close();
		});

		var set = $("[data-var=set");

		var colors = ["green", "yellow", "blue", "red"];
		var teams = ["north", "south"];

		var playerNames = {
			green: $("[data-color=green][data-var=name"),
			yellow: $("[data-color=yellow][data-var=name"),
			blue: $("[data-color=blue][data-var=name"),
			red: $("[data-color=red][data-var=name")
		};

		var serving = {
			green: $("[data-color=green][data-var=serving"),
			yellow: $("[data-color=yellow][data-var=serving"),
			blue: $("[data-color=blue][data-var=serving"),
			red: $("[data-color=red][data-var=serving")
		};

		var scores = {
			north: $("[data-team=north][data-var=score"),
			south: $("[data-team=south][data-var=score")
		};

		var scoreAudio = new PingPongSound(
			"boing.wav",
			"bump.wav",
			"picking-up.wav",
			"coin.wav",
			"spring-jump.wav",
			"pacman-chomp.wav"
		);

		function update(data){
			if(data == null) return;
			if(data.matchId != matchId) return;

			set.html(data.game);

			for(var i in colors){
				var color = colors[i];
				playerNames[color].html(data.players[color].playerName);

				if(data.players[color].serving){
					serving[color].addClass("active");
				} else {
					serving[color].removeClass("active");
				}
			}

			for(var i in teams){
				var team = teams[i];
				var previousScore = parseInt(scores[team].html());
				var nextScore = parseInt(data.teams[team].points);

				scores[team].html(pad(data.teams[team].points));
				if(previousScore != nextScore){
					scores[team].addClass("scored");
					scoreAudio.play();
				}
			}
			setTimeout(function(){
				for(side in scores){
					scores[side].removeClass("scored");
				}
			}, 2000);

			for(var side in data.teams){
				var team = data.teams[side];

				var cells = $("tr[data-teamid=" + team.teamId + "]").find("td");
				cells.eq(0).html(team.playerName);

				for(var i = 0; i < team.games.length; i++){
					var game = team.games[i];
					var cell = cells.eq(i + 1).html("").removeClass("win");

					if(game.score != null){
						cell.html(pad(game.score));
						if(game.win){
							cell.addClass("win");
						}
					}
				}
			}

			sayings(data.teams.south.points, data.teams.north.points);

			if(data.complete){
				if(data.teams.north.winner){
					teamId = data.teams.north.teamId;
				} else if(data.teams.south.winner){
					teamId = data.teams.south.teamId;
				}

				if(data.teams.north.winner || data.teams.south.winner){
					$("tr[data-teamid=" + teamId + "]").find("td").first().append(" - <strong>Winner!</strong>");
				}

				$(".complete-hide").addClass("hidden");
				$(".complete-show").removeClass("hidden");
			}
		}

		var randomize = $("input[name=randomize]");

		$("button.randomize").on("click", function(){
			var source = $(this);

			if(randomize.val() == "true"){
				source.html("Yes");
				randomize.val("false");
			} else {
				source.html("No");
				randomize.val("true");
			}
		});

		enableUndo();

	}

});
