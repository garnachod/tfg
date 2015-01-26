jQuery( document ).ready(function( $ ) {
	$("#form1").submit(function(e) {
		e.preventDefault();
		var valueSearch = $("#input_search").val();
		var valueAleat = $("#input_aleat").is(':checked');
		
		var dataEnvio = { search: valueSearch, aleat: valueAleat };

		busqueda.doSearch(dataEnvio);
	});
	$("#bot_no_usar").click(function(e){
		e.preventDefault();
		alert('no usar');
	});
	$("#bot_no_relevante").click(function(e){
		e.preventDefault();
		alert('no relevante');
	});
	$("#bot_relevante").click(function(e){
		e.preventDefault();
		alert('relevante');
	});


	//inicializacion
	busqueda.inicializa();
	//
	$("#cont_tweet_bot").hide();
});

var busqueda = {
	urlApi : '',
	urlSearch: '',
	progressBar:null,


	inicializa: function(){
		/*
		cadena += '<div class="busqueda-cont" id="asincData">'
		
		cadena += '</div>'

		*/
		busqueda.urlSearch = busqueda.urlApi + 'busqueda_tweet_train';
		/*busqueda.progressBar = new ProgressBar.Circle('#progress_bar', {
    		strokeWidth: 3,
    	
		});*/
	},
	doSearch:function(dataEnvio){
		/*busqueda.progressBar.set(0);
		busqueda.progressBar.animate(1, {
			from: { color: '#2DCCD3' },
	    	to: { color: '#0085AD' },
	    	step: function(state, circle) {
	        	circle.path.setAttribute('stroke', state.color);
	    	},
	    	duration: 10000
		}, function() {
	    	
		});	*/
		
		var consulta = $.post(busqueda.urlSearch, dataEnvio, busqueda.onSucces, "json");
		consulta.fail(busqueda.onFail);
	},

	onSucces: function(data){
		console.log('post done');
		if(data.status == "true"){
			var tweets = data.tweets;

			for (var i = tweets.length - 1; i >= 0; i--) {

				Tweet.contructorFromJSON(tweets[i]);

				$('#cont_tweet').html(Tweet.toHTML);
				$("#cont_tweet_bot").show();
			};

			//setTimeout(busqueda.doSearch, 10000);
			//$('#status_asinc').html('<h3>Busqueda en marcha</h3>');
			
			
			
		}else{
			busqueda.onFail(null);
		}
		
	},

	onFail:function(data){
		/*$('#status_asinc').html('<h3>Se ha terminado la busqueda</h3>');
		busqueda.progressBar.set(1);*/
	}
};

