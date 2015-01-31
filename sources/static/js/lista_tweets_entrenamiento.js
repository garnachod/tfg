jQuery( document ).ready(function( $ ) {
	
	votar.inicializa();

});

var votar = {
	urlApi : '',
	urlSearch: '',
	inicializa: function(){
		votar.urlSearch = votar.urlApi + 'change_tweet_train';
	},
	cambiarVotoID: function(id){
		var dataEnvio = {change: id};
		votar.doSend(dataEnvio);
	},
	doSend:function(dataEnvio){
		var consulta = $.post(votar.urlSearch, dataEnvio, votar.onSucces, "json");
		consulta.fail(votar.onFail);
	},
	onSucces: function(data){
		if(data.status == "true"){
			var clase = $('#'+data.identificador).attr('class');
			if(clase == 'no_relevante'){
				$( '#'+data.identificador).removeClass('no_relevante');
				$( '#'+data.identificador).addClass('relevante');
			}else{
				$( '#'+data.identificador).removeClass('relevante');
				$( '#'+data.identificador).addClass('no_relevante');
			}
			
		}else{
			
		}
		
	},
	onFail:function(data){
		
	}
}