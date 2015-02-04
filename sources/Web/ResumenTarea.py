# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from MachineLearning.EntrenamientoTweets import EntrenamientoTweets
from MachineLearning.EntrenamientoTweets import EntrenamientoTweets_ASINC
from flask import Flask, session
from Tweet import Tweet
import json

class ResumenTarea(object):
	"""docstring for ResumenTarea"""
	def __init__(self):
		super(ResumenTarea, self).__init__()
		self.head = Head('Resumen Entrenamiento')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/estadisticas.css")
		self.head.add_css("static/css/resumen_tarea.css")
		self.head.add_css("static/css/busqueda.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/Chart.min.js")
		self.head.activaMenu()

	def toString(self, identificador):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-general">
							<h3 style="text-align: left;" >Resumen tarea</h3>'''

		#información genérica de la tarea
		#cadena += '<div class="tweets_recuperados">'
		cadena += '''
					<div class="contenedor-estadistica" style="width: 100%; ">	
					<p class="titulo-estadistica">Frecuencia diaria de tweets recuperados</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweets" width="1000" height="300"/>
						</div>
					</div>
				  '''


		#información especifica
		tipo = self.consultas.getTipoTarea(identificador)
		if "BusquedaSencilla" in tipo:
			cadena += self.toStringBusquedaSencilla(identificador)
		

		
		cadena +='''</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()

		cadena += '<script>'
		cadena += self.generaGraficaFrecuenciasDiarias(identificador)
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaOnLoad()
		cadena += '</script>'

		cadena += '</body>'

		return cadena

	def toStringBusquedaSencilla(self, identificador):
		cadena = '<h3 style="text-align: left;" >Tweets</h3>'
		cadena += '<div style="text-align: left;">'
		tweets = self.consultas.getTweetsRecuperadosTareaID(identificador)

		for tweet in tweets:
			cadena += Tweet.imprimeTweett(tweet, False)
		cadena += '</div>'

		return cadena

	def generaGraficaFrecuenciasDiarias(self, identificador):
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