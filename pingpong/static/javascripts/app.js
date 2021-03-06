$(function(){

	$("form.action-delete").on("submit", function(){
		return confirm("Are you sure you want to delete this?");
	});

	$("#season-filter").on("change", function(){
		$(this).parent("form").submit();
	});

	var playerFilter = $("#matches-player-filter").on("change", matchesfilters);
	var opponentFilter = $("#matches-opponent-filter").on("change", matchesfilters);
	var matchTypeFilter = $("#matches-match-type-filter").on("change", matchesfilters);
	var seasonFilter = $("#matches-season-filter").on("change", matchesfilters);
	function matchesfilters(){
		var params = [];

		var playerId = playerFilter.val();
		var opponentId = opponentFilter.val();
		var matchType = matchTypeFilter.val();
		var season = seasonFilter.val();

		if(playerId.length){
			params.push("playerId=" + playerId);
		}

		if(opponentId.length){
			params.push("opponentId=" + opponentId);
		}

		if(matchType.length){
			params.push("matchType=" + matchType);
		}

		if(season.length){
			params.push("season=" + season);
		}

		window.location = "/matches" + (params.length ? "?" : "") + params.join("&");
	}

	$(".alert-dismissible").each(function(){
		var source = $(this);

		if(source.hasClass("auto-close")){
			setTimeout(function(){
				source.fadeOut();
			}, 3000);
		}

		source.find(".close").on("click", function(){
			source.fadeOut("fast");
		});
	});

	jQuery.fn.extend({
		exists: function(){
			return this.length > 0;
		}
	});

	var setOfficeForm = $("#set-office-form");
	var setOfficeField = $("#set-office-field");
	setOfficeField.on("change", function(){
		setOfficeForm.submit();
	});

});

function domain(){
	return "http://" + document.domain + ":" + location.port
}

function disableUndo(){
	$(document).unbind("keypress");
}

function enableUndo(){
	var matchId = $("#singles, #doubles, #nines").data("matchid");
	$(document).on("keypress", function(e){
		if(e.which == 117){
			$.post("/matches/" + matchId + "/undo");
		}
	});
}

function shuffle(a) {
	for (let i = a.length; i; i--) {
		let j = Math.floor(Math.random() * i);
		[a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
}

function pad(num){
	return ("00" + num).substr(-2,2);
}

function randRange(min, max){
	return Math.floor(Math.random() * (max - min + 1)) + min;
}
