# -*- coding: utf-8 -*-
class MenuSlide(object):
	"""docstring for MenuSlide"""
	def __init__(self):
		self.menu = True

	def getCSSLib(self):
		return "static/css/jquery.mmenu.all.css"

	def getJSLib(self):
		return "static/js/jquery.mmenu.min.all.js"

	def getJSCode(self):
		code = '<script type="text/javascript">'
		code +=	'$(function() {'
		code +=	'	$("nav#menu").mmenu();'
		code +=	'});'
		code += '</script>'

		return code

	def toStringHead(self):
		return '<a href="#menu"></a>'

	def toStringContenido(self):
		cadena =('<nav id="menu">'
					'<ul>'
					'<li><a href="/">Búsqueda</a></li>'
					'<li><a href="/planificartarea">Planificar Tareas</a></li>'
					'<li><a href="/ver_tareas_pendientes">Ver Tareas pendientes</a></li>'
					'<li><a href="/ver_tareas_finalizadas">Ver Tareas finalizadas</a></li>'
					'<li><a href="/lista_entrena_tweets">Listas de tweets de entrenamiento</a></li>'
					'<li><a href="/entrena_tweets">Entrenar usando tweets</a></li>'
					'<li><a href="/ver_entrena_tweets">Ver Tweets entrenamiento</a></li>'
					'<li><a href="/lanzar_entrenamientos">Lanzar entrenamientos</a></li>'
					'<li><a href="/estadisticas">Estadísticas generales</a></li>'
					'<li><a href="/contacto">Contacto</a></li>'
					'</ul>'
				'</nav>')

		return cadena
		