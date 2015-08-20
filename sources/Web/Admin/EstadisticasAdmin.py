# -*- coding: utf-8 -*-
from Web.Head import Head
from Web.UserHeader import UserHeader
from flask import Flask, session
from DBbridge.ConsultasWeb import ConsultasWeb
from Web.SupportWeb import SupportWeb
from WebPageAdmin import WebPageAdmin
import json

class EstadisticasAdmin(WebPageAdmin):
	"""docstring for VisualizarListaTareas"""
	def __init__(self):
		super(EstadisticasAdmin, self).__init__()
		self.head.setTitulo('Estadisticas')
	
	def insertStyles(self):
		self.head.add_css("/static/css/general.css")
		self.head.add_css("/static/css/admin.css")
		self.head.add_css("/static/css/estadisticas.css")

	def insertScripts(self):
		#self.head.add_js("/static/js/jquery.js")
		self.head.add_js("/static/js/Chart.min.js")


	def mid(self):
		mid = '<h3 style="text-align: left;" >Estadísticas de tweets</h3>'


		mid += '''
					<div class="contenedor-estadistica contenedor-pie">	
					<p class="titulo-estadistica">Número de Tweets son RT</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweetsRT" width="300" height="300"/>
						</div>
					</div>
				  '''

		mid += '''
					<div class="contenedor-estadistica contenedor-pie">	
					<p class="titulo-estadistica">Número de Tweets únicos, multimedia</p>
						<div id="canvas-holder">
							<canvas id="chart-numTweetsMedia" width="300" height="300"/>
						</div>
					</div>
				  ''' 

		mid += '<div style="overflow:hidden; width: 100%;">'
		mid += '<h3 style="text-align: left;" >Estadísticas de la aplicación</h3>'

		mid += '''
					<div class="contenedor-estadistica">	
						<p class="titulo-estadistica">Frecuencia de consultas diarias</p>
						<div id="canvas-holder">
							<canvas id="chart-consultas" width="1000" height="300"/>
						</div>
					</div>
				  '''
		mid += '</div>'

		return SupportWeb.addGeneralStructureMid(mid)

	def scripts(self):
		#cadena = menu.toStringContenido()
		
		cadena = '<script>'
		cadena += self.generaCodigoNumeroTweetsRT()
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaCodigoNumeroTweetsMedia()
		cadena += '</script>'
		cadena += '<script>'
		#cadena += self.generaCodigoPorcentajeErrorT()
		cadena += self.generaCodigoFrecuenciaConsultas()
		cadena += '</script>'
		cadena += '<script>'
		cadena += self.generaOnLoad()
		cadena += '</script>'

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
		no_rt, si_rt = self.consultas.getNumTweetsRT()
		objJson[0]["value"] = no_rt
		objJson[0]["color"] = '#949FB1'
		objJson[0]["highlight"] = '#A8B3C5'
		objJson[0]["label"] = 'Tweets que nos son RT'

		objJson.append({})
		objJson[1]["value"] = si_rt
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
		no_media , si_media = self.consultas.getNumTweetsMedia()
		objJson[0]["value"] = no_media
		objJson[0]["color"] = '#949FB1'
		objJson[0]["highlight"] = '#A8B3C5'
		objJson[0]["label"] = 'No tienen Multimedia'

		objJson.append({})
		objJson[1]["value"] = si_media
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

	def generaCodigoFrecuenciaConsultas(self):
		rows = self.consultas.getEstadisticaUsoAplicacionConsultas()

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

		cadena = "var numConsultas = " + json.JSONEncoder().encode(objJson)

		return cadena
	
	def generaOnLoad(self):
		cadena = '''
					window.onload = function(){
						console.log("lanzado");
						var ctx = document.getElementById("chart-numTweetsRT").getContext("2d");
						window.myPieNumTweetsRT = new Chart(ctx).Pie(numTweetsRT, {responsive : true});
						var ctx2 = document.getElementById("chart-numTweetsMedia").getContext("2d");
						window.myPieNumTweetsMedia = new Chart(ctx2).Pie(numTweetsMedia , {responsive : true});
						var ctx3 = document.getElementById("chart-consultas").getContext("2d");
						window.myPieConsultas = new Chart(ctx3).Line(numConsultas, {responsive : true});
					};
				  '''
		return cadena
