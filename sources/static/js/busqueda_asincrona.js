jQuery( document ).ready(function( $ ) {
// Code using $ as usual goes here.
	busqueda.inicializa();
	busqueda.doSearchSinc();
	$('#cargar-mas').click(function(event){
		event.preventDefault();
		busqueda.doSearchSinc();
	});
});


var allTweets = {
	listTweetsShow: new Array(),
	listTweetsSinc: new Array(),
	listTweetsASinc: new Array(),
	numTweetsShow: 0,
	numTweetsSinc: 0,
	numTweetsASinc: 0,
	min_id: 0,
	frame: null,

	inicializa:function(){
		//allTweets.frame = new Sly('#frame').init();
	},

	pushTweetsSinc:function(tweets){
		var l = tweets.length;
		for (var i = 0; i < l; i++) {
			allTweets.listTweetsSinc.push(tweets[i]);
			allTweets.numTweetsSinc++;
			Tweet.contructorFromJSON(tweets[i]);
			$('#tweets').append(Tweet.toHTML(true));
			id_tweet = tweets[i].id_tweet;

			if(allTweets.min_id == 0){
				allTweets.min_id = id_tweet;
			}else if (allTweets.min_id > id_tweet) {
				allTweets.min_id = id_tweet;
			}
		};
	},
	pushTweetsAsinc:function(tweets){
		var l = tweets.length;
		for (var i = 0; i < l; i++) {
			allTweets.listTweetsASinc.push(tweets[i]);
			allTweets.numTweetsASinc++;
		};
	},
	getMenorIdTweetsSinc:function(){
		return allTweets.min_id;
	}

};

var busqueda = {
	urlApi : '',
	urlSearchAsinc: '',
	urlSearchSinc: '',
	progressBar:null,
	active_cargar_mas:false,


	inicializa: function(){
		/*
		cadena += '<div class="busqueda-cont" id="asincData">'
		
		cadena += '</div>'

		*/
		busqueda.urlSearch = busqueda.urlApi + 'busqueda_asinc';
		busqueda.urlSearchSinc = busqueda.urlApi + 'busqueda_sinc';
		busqueda.progressBar = new ProgressBar.Circle('#progress_bar', {
    		strokeWidth: 3,
    	
		});
		busqueda.active_cargar_mas = true;
	},
	doSearchAsinc:function(){
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

	doSearchSinc:function(){
		if(!busqueda.active_cargar_mas){
			return;
		}
	
		var consulta = $.post(
			busqueda.urlSearchSinc,
			{
				num_tweets: 50,
				tipo_busqueda: tipo,
				search_id: searchID,
				max_id:allTweets.getMenorIdTweetsSinc()
			},
			busqueda.onSuccesSinc, "json");
		busqueda.active_cargar_mas = false;
		consulta.fail(busqueda.onFail);
		
	},
	onSucces: function(data){
		console.log('post done');
		if(data.status == "true"){
			var tweets = data.tweets;
			allTweets.pushTweetsAsinc(tweets);

			//setTimeout(busqueda.doSearchSinc, 10000);
			//$('#status_asinc').html('<h3>Busqueda en marcha</h3>');
			
			
			
		}else{
			busqueda.onFail(null);
		}
		
	},
	onSuccesSinc: function(data){
		console.log('post done');
		if(data.status == "true"){
			busqueda.active_cargar_mas = true;
			var tweets = data.tweets;
			allTweets.pushTweetsSinc(tweets);

			/*for (var i = tweets.length - 1; i >= 0; i--) {
								
				//Tweet.contructorFromJSON(tweets[i]);

				//$('#asinc_tweets').append(Tweet.toHTML);
			};*/

			//setTimeout(busqueda.doSearchAsinc, 10000);
			//$('#status_asinc').html('<h3>Busqueda en marcha</h3>');
			
			
			
		}else{
			busqueda.onFail(null);
		}
		
	},

	onFail:function(data){
		$('#status_asinc').html('<h3>Se ha terminado la busqueda</h3>');
		busqueda.progressBar.set(1);
	}
};
