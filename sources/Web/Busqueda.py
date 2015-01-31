# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from busquedaApi.AsincSearch import AsincSearch
from Tweet import Tweet
import hashlib
import time

class Busqueda():
	def __init__(self):
		self.consultas = ConsultasWeb()
		self.head = Head('Resultado busqueda')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/busqueda.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/progressbar.min.js")
		self.head.add_js("static/js/tweet.js")
		self.head.add_js("static/js/busqueda_asincrona.js")
		

	def doBusqueda(self, tipo, texto):
		if tipo == 'suser' or tipo == 'topic':
			#print session['user_id']
			searchID = self.consultas.setAppSearchAndGetId(texto, session['user_id'])
			t = AsincSearch(tipo, texto, session['user_id'], searchID)
			t.start()

			return searchID
		else:
			return 'ERR'

	def toString(self, tipo, texto):
		cadena =  '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'
	
		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(session["username"], 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']))
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '<div class="mid"><div class="mid-cont">'
		cadena += '<div class="busqueda-cont" id="asincData">'
		cadena += '<div id="status_asinc">'
		cadena += '</div>'
		cadena += '<div id="progress_bar">'
		cadena += '</div>'
		cadena += '<div id="asinc_tweets">'
		cadena += '</div>'
		cadena += '</div>'

		cadena += '<div class="busqueda-cont">'
		cadena += '<h3>Datos Cargados en la base de datos</h3>'
						
		
		#cada tipo hace una busqueda a la base de datos y se imprime
		if tipo == 'suser':
			cadena += self.toStringSUser(texto)
		elif tipo == 'topic':
			lista_keywords = texto.replace(", ", ",").split(",")
			cadena += self.toStringSTopic(lista_keywords)
		else:
			return 'ERR'

		#se cierran los div y se retorna la cadena
		cadena += '</div>'
		cadena +='</div></div>'

		cadena += '</body>'
		return cadena

	def toStringSUser(self, user):
		arrayTweets = self.consultas.getTweetsUsuario(user)
		cadena  = ''
		for tweet in arrayTweets:
			cadena += Tweet.imprimeTweett(tweet)

		return cadena

	def toStringSTopic(self, topics):
		arrayTweets = self.consultas.getTweetsTopics(topics)
		cadena  = ''
		for tweet in arrayTweets:
			cadena += Tweet.imprimeTweett(tweet)

		return cadena

         