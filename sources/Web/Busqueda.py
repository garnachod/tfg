# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from busquedaApi.AsincSearch import AsincSearch
from Tweet import Tweet
from WebPageMenu import WebPageMenu
from SupportWeb import SupportWeb
import hashlib
import time

class Busqueda(WebPageMenu):
	def __init__(self):
		super(Busqueda, self).__init__()
		self.head.setTitulo('Busqueda')


	def insertStyles(self):
		self.head.add_css("static/css/busqueda.css")
		self.head.add_css("static/css/general.css")


	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/progressbar.min.js")
		#self.head.add_js("static/js/sly.min.js")
		self.head.add_js("static/js/tweet.js")
		self.head.add_js("static/js/busqueda_asincrona.js")

		

	def doBusqueda(self, tipo, texto):
		if tipo == 'suser' or tipo == 'topic':
			#print session['user_id']
			self.searchID = self.consultas.setAppSearchAndGetId(texto, session['user_id'])
			t = AsincSearch(tipo, texto, session['user_id'], self.searchID)
			t.start()

			return self.searchID
		else:
			return 'ERR'

	def toString(self, tipo, texto):
		self.tipo = tipo
		self.texto = texto
		return super(Busqueda, self).toString()

	def mid(self):
		cadena = '<div id="status_asinc">'
		cadena += '</div>'
		cadena += '<div id="progress_bar">'
		cadena += '</div>'

		cadena += '<div id="tweets" style="text-align:left;">'
		cadena += '</div>'

		return SupportWeb.addGeneralStructureMid(cadena)


	def scripts(self):
		cadena = '<script>'
		cadena += 'var tipo = "' +str(self.tipo)+ '";'
		cadena += 'var lastTweet = ' +str(-1)+ ';'
		cadena += 'var searchID = ' +str(self.searchID)+ ';'
		cadena += '</script>'
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

         