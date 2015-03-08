# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from MachineLearning.EntrenamientoTweets import EntrenamientoTweets
from MachineLearning.EntrenamientoTweets import EntrenamientoTweets_ASINC
from flask import Flask, session
import json

class LanzarEntrenamiento(object):
	"""docstring for VisualizarListaTareas"""
	def __init__(self):
		super(LanzarEntrenamiento, self).__init__()
		self.head = Head('Lanzar Entrenamiento')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		#self.head.add_css("static/css/estadisticas.css")
		self.head.add_js("static/js/jquery.js")
		#self.head.add_js("static/js/Chart.min.js")
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
							<div class="cont-general">
							<h3 style="text-align: left;" >Lanzar entrenamiento Tweets</h3>'''

		rows = self.consultas.getListasEntrenamiento()
		for row in rows:
			cadena += '<a class="boton-general" href="/lanzar_entrenamientos?id_entr='+str(row[0])+'">' + row[1] +'</a>'

		
		cadena +='''</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()

		cadena += '</body>'

		return cadena

	def generaEntrenamientoTweets(self, identificador):
		asinc = EntrenamientoTweets_ASINC(identificador)
		asinc.start()
		#entre = EntrenamientoTweets()
		#entre.lanzar(identificador)
		return 'OK'
