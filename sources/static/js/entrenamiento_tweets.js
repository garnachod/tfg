jQuery( document ).ready(function( $ ) {
	$("#form1").submit(function(e) {
		e.preventDefault();
		getSearchAndSend();
	});
	$("#bot_no_usar").click(function(e){
		e.preventDefault();
		var id_lista = $("#lista_entrenamiento").val();
		var dataEnvio = {vote: "no_usar", lista:id_lista};

		votar.doSend(dataEnvio);
	});
	$("#bot_no_relevante").click(function(e){
		e.preventDefault();
		var id_lista = $("#lista_entrenamiento").val();
		var dataEnvio = {vote: "no_relevante", lista:id_lista};
		votar.doSend(dataEnvio);
	});
	$("#bot_relevante").click(function(e){
		e.preventDefault();
		var id_lista = $("#lista_entrenamiento").val();
		var dataEnvio = {vote: "relevante", lista:id_lista};
		votar.doSend(dataEnvio);
	});


	//inicializacion
	busqueda.inicializa();
	votar.inicializa();
	//
	$("#cont_tweet_bot").hide();
});

function getSearchAndSend(){
	var valueSearch = $("#input_search").val();
	var valueAleat = $("#input_aleat").is(':checked');
	var id_lista = $("#lista_entrenamiento").val();
	
	var dataEnvio = { search: valueSearch, aleat: valueAleat, lista:id_lista};

	busqueda.doSearch(dataEnvio);
}

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

				$('#cont_tweet').html(Tweet.toHTML(false));
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

var votar = {
	urlApi : '',
	urlSearch: '',
	inicializa: function(){
		votar.urlSearch = votar.urlApi + 'set_tweet_train';
	},
	doSend:function(dataEnvio){
		var consulta = $.post(votar.urlSearch, dataEnvio, votar.onSucces, "json");
		consulta.fail(votar.onFail);
	},
	onSucces: function(data){

		if(data.status == "true"){
			getSearchAndSend();	
		}else{
			busqueda.onFail(null);
		}
		
	},
	onFail:function(data){
		$("#cont_tweet_bot").hide();
	}
}