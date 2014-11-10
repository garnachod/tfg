jQuery( document ).ready(function( $ ) {
// Code using $ as usual goes here.
	busqueda.inicializa();
	busqueda.doSearch();
});

var Tweet = {
	rt:'',
	twitter_user:'',
	is_rt:false,
	texto:'',
	fav:'',
	media_url:'',

	/*
	{
	    "rt": "12",
	    "tuser": "vmwarehorizon",
	    "is_rt": "False",
	    "text": "We're super excited about our collaboration with @googlechrome @nvidia to bring high end workstation graphics to a Chromebook #vmworld",
	    "fav": "11",
	    "media": ""
	}
	*/
	contructorFromJSON:function(tweet){
		Tweet.rt = tweet.rt;
		Tweet.twitter_user = tweet.tuser;
		if(tweet.is_rt == "False"){
			Tweet.is_rt = false;
		}else{
			Tweet.is_rt = true;
		}
		Tweet.texto = tweet.text;
		Tweet.fav = tweet.fav;
		Tweet.media_url = tweet.media;
	},

	toHTML:function(){
		var cadena = '<div class="delimitador"></div>';
		cadena += Tweet.relevanciaToHTML();
		cadena += Tweet.usrImgToHTML();
		cadena += '<div class="cont-tweet">';
		cadena += Tweet.tweetUsrToHTML();
		cadena += '<div class="tweet-text">';
		cadena += Tweet.textoToHTML();
		cadena += '</div>';
		cadena += '<div class="contenedor-rf">';
		cadena += '<span class="fav-count">';
		cadena += Tweet.fav;
		cadena += '</span>';
		cadena += '<span class="retweet-count">';
		cadena += Tweet.rt;
		cadena += '</span>';
		cadena += '</div>';
		//#tiene algún tipo de objeto multimedia
		if (Tweet.media_url != ''){
			cadena += Tweet.multimediaToHTML();
		}
		cadena += '</div>';

		

		cadena += '</div>';
		return cadena;
	},

	relevanciaToHTML : function(){
		return '<div class="tweet">';
	},
	usrImgToHTML:function(){
		var cadena = '<div class="cont-user-img">';
		cadena += '<img src="static/img/tweetuser.png">';
		cadena += '</div>';
		return cadena;
	},
	tweetUsrToHTML :function(){
		var cadena = '<div class="cont-usr">';
		cadena += '<a href="https://twitter.com/'+Tweet.twitter_user+'" target="_blank">@'+Tweet.twitter_user+ '</a>';
		cadena += '</div>';
		return cadena;
	},

	textoToHTML : function(){
		var palabras = Tweet.texto.split(" ");
		var cadena = '';

		var tam = palabras.length;
		var palabra;
		for (var i = 0; i < tam; i++) {
			palabra = palabras[i];

			if((palabra.indexOf("http://") > -1) || (palabra.indexOf("https://") > -1)){
				cadena += '<a class="link" href="'+ palabra+'" target="_blank">'+palabra+'</a> ';
			}else if(palabra.indexOf("@") > -1){
				var user = Tweet.limpiaTwitterUser(palabra);
				cadena += '<a class="user" href="https://twitter.com/'+ user +'" target="_blank">'+palabra+'</a> ';
			}else{
				cadena += palabra + " ";
			}
			
		}
		return cadena;
	},

	multimediaToHTML:function(){

		var cadena = '';

		if((Tweet.media_url.indexOf(".jpg") > -1) || (Tweet.media_url.indexOf(".png") > -1)){
			cadena += '<div class="cont-multi">';
			cadena += '<a href="'+ Tweet.media_url +'" target="_blank">';
			cadena += '<div class="img_busqueda" style="background-image: url(\'';
			//#http://pbs.twimg.com/media/BziK-yaIIAA1uW2.jpg
			cadena += Tweet.media_url;
			cadena += '\');">';
		
			cadena += '</div>';
			cadena += '</a>';
			cadena += '</div>';
		}
		return cadena;
	},
	limpiaTwitterUser : function(user){
		var cadena = '';

		for (var i = user.length - 1; i >= 0; i--) {
			caracter = user[i];
			if(caracter != '@' && caracter != ':'){
				cadena = caracter + cadena;
			}
		};

		return cadena;
	}
};




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
