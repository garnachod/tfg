# -*- coding: utf-8 -*-
from Head import Head
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from MenuSlide import MenuSlide
from flask import Flask, session
from Tweet import Tweet

class ListarTweetsEntrenamiento(object):
	"""docstring for ListarTweetsEntrenamiento"""
	def __init__(self):
		super(ListarTweetsEntrenamiento, self).__init__()
		self.consultas = ConsultasWeb()
		self.head = Head('Tweets de entrenamiento')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/index.css")
		self.head.add_css("static/css/busqueda.css")
		self.head.add_css("static/css/lista_tweets_train.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/lista_tweets_entrenamiento.js")
		self.head.activaMenu()

	def toString(self, identificador = -1):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		#tweets = self.consultas.getTweetsEntrenamientoListar()
		#if tweets == False:
		#	return 'ERR'
		

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-busqueda">
				'''
		if identificador == -1:
			rows = self.consultas.getListasEntrenamiento()
			cadena += '<h3 style="text-align:  left;">Seleccionar lista de entrenamiento:</h3>'
			if rows == False:
				return 'ERR'
			
			for row in rows:
				#insertar el link
				link = '/ver_entrena_tweets?id_lista=' + str(row[0])
				cadena += '<p><a href="'+link+'" class="boton-general">' + row[1] + '</a></p>'
		else:
			tweets = self.consultas.getTweetsEntrenamientoListar(identificador)
			cadena += '<h3 style="text-align:  left;">tweets</h3>'
			if tweets == False:
				return 'ERR'

			for tweet in tweets:
				clase = self.privateTweetDBGetClass(tweet)
				if clase == 'no_relevante':
					cadena += '<div id="'+ str(self.privateTweetDBGetId(tweet))+ '" class="no_relevante">'
					cadena += Tweet.imprimeTweett(tweet, False)
					cadena += '<div style="text-align:center;">'
					cadena += '<a href="javascript:votar.cambiarVotoID('+str(self.privateTweetDBGetId(tweet)) +')" class="boton-general" style="margin-bottom: 10px;">Cambiar voto</a>'
					cadena += '</div>'
					cadena += '</div>'
				else:
					cadena += '<div id="'+ str(self.privateTweetDBGetId(tweet)) + '" class="relevante">'
					cadena += Tweet.imprimeTweett(tweet, False)
					cadena += '<div style="text-align:center;">'
					cadena += '<a href="javascript:votar.cambiarVotoID('+str(self.privateTweetDBGetId(tweet)) +')" class="boton-general" style="margin-bottom: 10px;">Cambiar voto</a>'
					cadena += '</div>'
					cadena += '</div>'


		cadena +=  '''
							</div>
						</div>
					</div>'''
		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body></html>'
		return cadena


	def privateTweetDBGetClass(self, tweet):
		longitud = len(tweet)
		return tweet[longitud-1]
	
	def privateTweetDBGetId(self, tweet):
		longitud = len(tweet)
		return tweet[longitud-2]

		