# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from flask import Flask, session
from SupportWeb import SupportWeb
from WebPageMenu import WebPageMenu
import json

class EntrenamientoTweet(WebPageMenu):
	"""docstring for EntrenamientoTweet"""
	def __init__(self):
		super(EntrenamientoTweet, self).__init__()
		self.head.setTitulo('Entrenamiento')
	
	def insertStyles(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/busqueda.css")

	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/tweet.js")
		self.head.add_js("static/js/entrenamiento_tweets.js")

	def mid(self):
		mid = self.generaNuevaListaEntrenamiento()
		mid += self.generaBusqueda()
		mid += self.generaEntrenamiento()

		

		return SupportWeb.addGeneralStructureMid(mid)


	def generaNuevaListaEntrenamiento(self):
		mid = '<h3 style="text-align: left;">Crear una lista de entrenamiento:</h3>'

		mid += '''
					<form method="post">
						Nombre de la lista: 
						<input id="nlista" type="text" name="nlista" placeholder="Nombre" style="text-align: left;">
						<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Crear"></p>
					</form>
				'''
		return mid

	def generaBusqueda(self):
		mid = '''
				<h3 style="text-align:  left;">Búsqueda:</h3>
					<form id="form1" action="" method="post">
							<input id="input_search" type="text" name="search" placeholder="#hashtag,palabra1,p1 p2">
							<input id="input_aleat" type="checkbox" name="aleat">Aleatorio'''
  		
  		#array 0 id, 1 nombre
  		#lista de entrenamientos
  		listas = self.consultas.getListasEntrenamiento()
  		mid += ('	<p>'
  				'		<select name="lista_entrenamiento" id="lista_entrenamiento" style="width: 325px;text-align: center;">')

  		for lista in listas:
  			mid += '<option value="'+str(lista[0])+'">'+str(lista[1])+'</option>'

  		mid += ('		</select>'
  				'	</p>'
  				'	<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Buscar"></p>'
				'</form>')

  		return mid

	def generaEntrenamiento(self):
		mid = '''
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
		return mid

	def scripts(self):
		return ''