# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from flask import session
from SupportWeb import SupportWeb
import json

class EntrenamientoTweets(object):
	"""docstring for EntrenamientoTweets"""
	def __init__(self):
		super(EntrenamientoTweets, self).__init__()
		self.head = Head('Entrenamiento')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/busqueda.css")
		#self.head.add_css("static/css/estadisticas.css")
		self.head.add_css("static/css/index.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/tweet.js")
		self.head.add_js("static/js/entrenamiento_tweets.js")
		#self.head.add_js("static/js/Chart.min.js")
		self.head.activaMenu()

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'
		
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		mid = '''
					<h3 style="text-align:  left;">Búsqueda:</h3>
					<form id="form1" action="" method="post">
							<input id="input_search" type="text" name="search" placeholder="#hashtag,palabra1,p1 p2">
							<input id="input_aleat" type="checkbox" name="aleat">Aleatorio'''
  		#array 0 id, 1 nombre
  		#lista de entrenamientos
  		listas = self.consultas.getListasEntrenamiento(session['user_id'])
  		mid += '<p><select name="lista_entrenamiento" id="lista_entrenamiento" style="width: 325px;text-align: center;">'
  		for lista in listas:
  			mid += '<option value="'+str(lista[0])+'">'+str(lista[1])+'</option>'

  		mid += '</select></p>'

		mid += '''<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Buscar"></p>
					</form>
				</div>
				<div class="cont-busqueda" style="text-align: left;">
					<h3 style="text-align:  left;">Tweet a entrenar:</h3>
					<div id="cont_tweet_bot">
						<div id="cont_tweet">

						</div>
						<div id="cont_bot" style="text-align: center;">
							<a id="bot_no_usar" href="" class="boton-general"> No usar tweet </a>
							<a id="bot_no_relevante" href="" class="boton-general"> No relevante </a>
							<a id="bot_relevante" href="" class="boton-general"> Relevante </a>
						</div>
					</div>
				'''

		cadena += SupportWeb.addGeneralStructureMid(mid)
			
		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body>'
		return cadena
		