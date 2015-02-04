# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from flask import Flask, session
import json

class Estadisticas(object):
	"""docstring for VisualizarListaTareas"""
	def __init__(self):
		super(Estadisticas, self).__init__()
		self.head = Head('Estadísticas')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/estadisticas.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/Chart.min.js")
		self.head.activaMenu()

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-estadisticas">
							<h3 style="text-align: left;" >Estadísticas de la aplicación</h3>'''


		cadena += '''
					<div class="contenedor-estadistica">	
					<p class="titulo-estadistica">Número de Tweets</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweetsRT" width="300" height="300"/>
						</div>
					</div>
				  '''

		cadena += '''
					<div class="contenedor-estadistica">	
					<p class="titulo-estadistica">Número de Tweets únicos, multimedia</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweetsMedia" width="300" height="300"/>
						</div>
					</div>
				  '''

		cadena += '<div style="overflow:hidden; width: 100%;">'
		cadena += '<h3 style="text-align: left;" >Estadísticas del entrenamiento</h3>'

		cadena += '''
					<div class="contenedor-estadistica">	
						<p class="titulo-estadistica">Fallo entrenamiento</p>
						<div id="canvas-holder">
							<canvas id="chart-porcentajeFalloT" width="300" height="300"/>
						</div>
					</div>
				  '''
		cadena += '</div>'
		cadena +='''</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()

		
		cadena += '<script>'
		cadena += self.generaCodigoNumeroTweetsRT()
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaCodigoNumeroTweetsMedia()
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaCodigoPorcentajeErrorT()
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaOnLoad()
		cadena += '</script>'
		cadena += '</body>'

		return cadena

	def generaCodigoNumeroTweetsRT(self):
		'''
			{
					value: 300,
					color:"#F7464A",
					highlight: "#FF5A5E",
					label: "Red"
			}
		'''

		objJson = []
		objJson.append({})
		objJson[0]["value"] = self.consultas.getNumTweetsNoRT()
		objJson[0]["color"] = '#949FB1'
		objJson[0]["highlight"] = '#A8B3C5'
		objJson[0]["label"] = 'Tweets que nos son RT'

		objJson.append({})
		objJson[1]["value"] = self.consultas.getNumTweetsSiRT()
		objJson[1]["color"] = '#46BFBD'
		objJson[1]["highlight"] = '#5AD3D1'
		objJson[1]["label"] = 'Tweets que son RT'

		cadena = "var numTweetsRT = " + json.JSONEncoder().encode(objJson)

		return cadena

	def generaCodigoNumeroTweetsMedia(self):
		'''
			{
					value: 300,
					color:"#F7464A",
					highlight: "#FF5A5E",
					label: "Red"
			}
		'''

		objJson = []
		objJson.append({})
		objJson[0]["value"] = self.consultas.getNumTweetsNoMedia()
		objJson[0]["color"] = '#949FB1'
		objJson[0]["highlight"] = '#A8B3C5'
		objJson[0]["label"] = 'No tienen Multimedia'

		objJson.append({})
		objJson[1]["value"] = self.consultas.getNumTweetsSiMedia()
		objJson[1]["color"] = '#46BFBD'
		objJson[1]["highlight"] = '#5AD3D1'
		objJson[1]["label"] = 'Tienen Multimedia'

		cadena = "var numTweetsMedia = " + json.JSONEncoder().encode(objJson)

		return cadena

	def generaCodigoPorcentajeErrorT(self):

		objJson = []
		objJson.append({})
		fallo = int(self.consultas.getPorcentajeFalloTrainTweets() *100)
		objJson[0]["value"] = fallo
		objJson[0]["color"] = '#949FB1'
		objJson[0]["highlight"] = '#A8B3C5'
		objJson[0]["label"] = 'Porcentaje de fallo'

		objJson.append({})
		objJson[1]["value"] = 100 - fallo
		objJson[1]["color"] = '#46BFBD'
		objJson[1]["highlight"] = '#5AD3D1'
		objJson[1]["label"] = 'Porcentaje de acierto'

		cadena = "var numProcentajeFalloT = " + json.JSONEncoder().encode(objJson)

		return cadena
	
	def generaOnLoad(self):
		cadena = '''
					window.onload = function(){
						var ctx = document.getElementById("chart-numTweetsRT").getContext("2d");
						window.myPieNumTweetsRT = new Chart(ctx).Pie(numTweetsRT);
						var ctx2 = document.getElementById("chart-numTweetsMedia").getContext("2d");
						window.myPieNumTweetsMedia = new Chart(ctx2).Pie(numTweetsMedia);
						var ctx3 = document.getElementById("chart-porcentajeFalloT").getContext("2d");
						window.myPieNumProcentajeFalloT = new Chart(ctx3).Pie(numProcentajeFalloT);
					};
				  '''
		return cadena
