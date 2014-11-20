jQuery( document ).ready(function( $ ) {
	$('#tipoBusqueda').on('change', function(){
		var opciones = new Array();
		opciones['suser'] = '@usuario';
		opciones['topic'] = 'uno,dos,dos tres';

		$('#input_search').attr("placeholder", opciones[this.value]);
	});
});