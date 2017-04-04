$(function(){

	$("#leaderboard").stupidtable();

	$(".leaderboard-player-container .nav-tabs li").on("click", function(){
		$(".leaderboard-player-container .nav-tabs li").removeClass("active");

		var source = $(this);
		source.addClass("active");

		$(".leaderboard-player-container .opponent-table").addClass("hidden");
		$(".leaderboard-player-container .opponent-table[data-matchtype=" + source.data("matchtype") + "]").removeClass("hidden");
	}).first().trigger("click");

	if($("#matches-new").length > 0){
		new Audio("/static/audio/bonus-game-match.wav").play();
	}

	if($("#matches-num-of-games").length > 0){
		new Audio("/static/audio/spring-jump.wav").play();
	}

	$("form.action-delete").on("submit", function(){
		return confirm("Are you sure you want to delete this?");
	});

});

function shuffle(a) {
	for (let i = a.length; i; i--) {
		let j = Math.floor(Math.random() * i);
		[a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
}

function pad(num){
	return ("00" + num).substr(-2,2);
}
