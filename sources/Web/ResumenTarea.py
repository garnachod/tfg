# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from MachineLearning.ClasificadorTweets import ClasificadorTweets
from flask import session
from Tweet import Tweet
from SupportWeb import SupportWeb
from WebPageMenu import WebPageMenu
import json

class ResumenTarea(WebPageMenu):
	"""docstring for ResumenTarea"""
	def __init__(self):
		super(ResumenTarea, self).__init__()
		self.head.setTitulo('Resumen Tarea')


	def insertStyles(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/estadisticas.css")
		self.head.add_css("static/css/resumen_tarea.css")
		self.head.add_css("static/css/busqueda.css")

	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/Chart.min.js")

	def toString(self, identificador):
		self.identificador = identificador
		return super(ResumenTarea, self).toString()

	def mid(self):
		mid = '<h3 style="text-align: left;" >Resumen tarea</h3>'

		#información genérica de la tarea
		#cadena += '<div class="tweets_recuperados">'
		mid += '''
				<div class="contenedor-estadistica" style="width: 100%; ">	
					<p class="titulo-estadistica">Frecuencia diaria de tweets recuperados</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweets" width="1000" height="300"/>
						</div>
					</div>
				  '''

		#información especifica
		tipo = self.consultas.getTipoTarea(self.identificador)
		self.analisisPalabras = False
		if "BusquedaSencilla" in tipo:
			mid += self.toStringBusquedaSencilla(self.identificador)
			self.analisisPalabras = False
		if "AnalisisPalabras" in tipo:
			mid += "<div>"
			mid += '<a href="/resumen_tarea?identificador='+str(self.identificador)+'&analizar=t" class="boton-general">Volver a analizar</a>'
			mid += "</div>"
			mid += self.toStringTweetsAnalisisPalabras(self.identificador)
			self.analisisPalabras = True

		return SupportWeb.addGeneralStructureMid(mid)

	def scripts(self):
		cadena = '<script>'
		cadena += self.generaGraficaFrecuenciasDiarias(self.identificador, self.analisisPalabras)
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaOnLoad()
		cadena += '</script>'

		cadena += '</body>'

		return cadena

	

	def toStringBusquedaSencilla(self, identificador):
		cadena = '<h3 style="text-align: left;" >Tweets</h3>'
		tweets = self.consultas.getTweetsRecuperadosTareaID(identificador)
		return cadena + self.toStringListaTweets(tweets)

	def toStringTweetsAnalisisPalabras(self, identificador):
		cadena = '<h3 style="text-align: left;" >Tweets relevantes</h3>'
		tweets = self.consultas.getTweetsRecuperadosTareaAnalisisID(identificador)
		return cadena + self.toStringListaTweets(tweets)

	def toStringListaTweets(self, tweets):
		cadena = '<div style="text-align: left;">'

		for tweet in tweets:
			cadena += Tweet.imprimeTweett(tweet, False)
		cadena += '</div>'

		return cadena

	def volverAnalizarTweets(self, identificador):
		search_id = self.consultas.getSearchIDFromIDTarea(identificador)
		tweets_id = self.consultas.getTweetsIdBusquedaTodos(search_id)
		id_lista = self.consultas.getIdListaEntrenamientoByIDSearch(search_id)
		clasificaTweet = ClasificadorTweets(id_lista)

		for row in tweets_id:

			clase = clasificaTweet.clasificaTweetById(row[0])
			self.consultas.editTweetAnalizado(row[0], clase)


		return self.toString(identificador)


	def generaGraficaFrecuenciasDiarias(self, identificador, analisisPalabras):
		rows = self.consultas.getTweetsAlDiaTarea(identificador)

		'''
		{
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }

		'''

		objJson = {}
		objJson['labels'] = []
		for row in rows:
			objJson['labels'].append(str(row[0]))

		objJson['datasets'] = []
		objAux = {}
		objAux['label'] = "Frecuencias diarias"
		objAux['fillColor'] = "rgba(151,187,205,0.2)"
		objAux['strokeColor'] = "rgba(151,187,205,1)"
		objAux['pointColor'] = "rgba(151,187,205,1)"
		objAux['pointStrokeColor'] = "#fff"
		objAux['pointHighlightFill'] = "#fff"
		objAux['pointHighlightStroke'] = "rgba(151,187,205,1)"
		objAux['data'] = []

		numRows = len(rows)
		for row in rows:
			objAux['data'].append(row[1])


		objJson['datasets'].append(objAux)

		if analisisPalabras == True:
			rows = self.consultas.getTweetsAlDiaTareaAnalisis(identificador)
			objAux = {}
			objAux['label'] = "Frecuencias diarias relevantes"
			objAux['fillColor'] = "rgba(105,105,105,0.2)"
			objAux['strokeColor'] = "rgba(105,105,105,1)"
			objAux['pointColor'] = "rgba(105,105,105,1)"
			objAux['pointStrokeColor'] = "#fff"
			objAux['pointHighlightFill'] = "#fff"
			objAux['pointHighlightStroke'] = "rgba(105,105,105,1)"
			objAux['data'] = []

			numRowsAux = len(rows)
			for i in range(numRows - numRowsAux):
				objAux['data'].append(0)

			for row in rows:
				objAux['data'].append(row[1])
			
			objJson['datasets'].append(objAux)

		
		cadena = "var numTweets = " + json.JSONEncoder().encode(objJson)

		return cadena

	def generaOnLoad(self):
		cadena = '''
					

					window.onload = function(){
						var ctx = document.getElementById("chart-numTweets").getContext("2d");
						window.myPieNumTweets = new Chart(ctx).Line(numTweets);
						
					};
				  '''
		return cadena