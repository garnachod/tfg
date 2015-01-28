jQuery( document ).ready(function( $ ) {
// Code using $ as usual goes here.
	busqueda.inicializa();
	busqueda.doSearch();
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
		busqueda.urlSearch = busqueda.urlApi + 'busqueda_asinc';
		busqueda.progressBar = new ProgressBar.Circle('#progress_bar', {
    		strokeWidth: 3,
    	
		});
	},
	doSearch:function(){
		busqueda.progressBar.set(0);
		busqueda.progressBar.animate(1, {
			from: { color: '#2DCCD3' },
	    	to: { color: '#0085AD' },
	    	step: function(state, circle) {
	        	circle.path.setAttribute('stroke', state.color);
	    	},
	    	duration: 10000
		}, function() {
	    	
		});	
		
		var consulta = $.post(busqueda.urlSearch, {}, busqueda.onSucces, "json");
		consulta.fail(busqueda.onFail);
	},

	onSucces: function(data){
		console.log('post done');
		if(data.status == "true"){
			var tweets = data.tweets;

			for (var i = tweets.length - 1; i >= 0; i--) {
				/*
				


				*/
				Tweet.contructorFromJSON(tweets[i]);

				$('#asinc_tweets').append(Tweet.toHTML);
			};

			setTimeout(busqueda.doSearch, 10000);
			$('#status_asinc').html('<h3>Busqueda en marcha</h3>');
			
			
			
		}else{
			busqueda.onFail(null);
		}
		
	},

	onFail:function(data){
		$('#status_asinc').html('<h3>Se ha terminado la busqueda</h3>');
		busqueda.progressBar.set(1);
	}
};
