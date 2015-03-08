jQuery( document ).ready(function( $ ) {
	$('#cont_lista_entrenamiento').hide();
	$('#tipoTarea').on('change', function(){
		//var opciones = new Array();
		//opciones['suser'] = '@usuario';
		//opciones['topic'] = 'uno,dos,dos tres';

		if(this.value == "sb"){
			$('#cont_lista_entrenamiento').hide();
		}else if(this.value == "bp"){
			$('#cont_lista_entrenamiento').show();
		}

		//$('#input_search').attr("placeholder", opciones[this.value]);
	});
});