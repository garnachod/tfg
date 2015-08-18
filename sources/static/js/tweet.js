var Tweet = {
	rt:'',
	twitter_user:'',
	is_rt:false,
	texto:'',
	fav:'',
	media_url:'',

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

		Tweet.media_urls = tweet.media;
		console.log(Tweet.media_urls);
		if(Tweet.media_urls != '' && Tweet.media_urls != 'None'){

			Tweet.media_urls = JSON.parse(Tweet.media_urls);
		}else{
			Tweet.media_urls = '';
		}
		Tweet.user_img = tweet.user_img;
	},

	toHTML:function(border){
		//var cadena = '<div class="delimitador"></div>';
		var cadena = '';
		cadena += Tweet.relevanciaToHTML(border);
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

		if (Tweet.media_urls != ''){
			cadena += Tweet.multimediaToHTML();
		}
		cadena += '</div>';

		

		cadena += '</div>';
		return cadena;
	},

	relevanciaToHTML : function(border){
		if (border == true)
			return '<div class="tweet border-tweet">';
		else
			return '<div class="tweet">';
	},
	usrImgToHTML:function(){
		var cadena = '<div class="cont-user-img">';
		cadena += '<img src="'+Tweet.user_img+'">';
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
		for (var i = 1; i <= 4; i++) {
			
			var key = 'photo_'+i;
            //alert("Mine is " + i + "|" + item.title + "|" + item.key);
            if(key in Tweet.media_urls){
				cadena += '<div class="cont-multi">';
				cadena += '<a href="'+ Tweet.media_urls[key] +'" target="_blank">';
				cadena += '<div class="img_busqueda" style="background-image: url(\'';
				//#http://pbs.twimg.com/media/BziK-yaIIAA1uW2.jpg
				cadena += Tweet.media_urls[key];
				cadena += '\');">';
			
				cadena += '</div>';
				cadena += '</a>';
				cadena += '</div>';
			}else{
				break;
			}
        };

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