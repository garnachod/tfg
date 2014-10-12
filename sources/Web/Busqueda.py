# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from DBbridge.ConsultasWeb import ConsultasWeb
from Skynet import Skynet
import hashlib

class Busqueda():
	def __init__(self):
		self.consultas = ConsultasWeb()
		self.head = Head('Resultado busqueda')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/busqueda.css")

	def doBusqueda(self, tipo, texto):
		if tipo == 'suser':
			skynet = Skynet(session['user_id'])
			skynet.research_user(texto);
		else:
			return 'ERR'

	def toString(self, tipo, texto):
		cadena =  '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'
		cadena += '''<div class="header">
						<div class="header-cont">
							
						</div>
					</div>
					<div class="mid">
						<div class="mid-cont">'''
		cadena += '<div class="busqueda-cont">'
						
		
		#cada tipo hace una busqueda a la base de datos y se imprime
		if tipo == 'suser':
			cadena += self.toStringSUser(texto)
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
			cadena += self.imprimeTweett(tweet)

		return cadena

	def imprimeTweett(self, tweet):
		palabras = tweet[0].split(" ")
		cadena = '<div class="delimitador"></div>'
		cadena += self.imprimeTweettRelevancia(tweet)
		cadena += '<div>'
		cadena += '<div class="tweet-text">'
		for palabra in palabras:
			#es un link
			if "http://" in palabra or "https://" in palabra:
				cadena += '<a class="link" href="'+ palabra+'" target="_blank">'+palabra+'</a> '
			#es un usuario de twitter
			elif "@" in palabra:
				cadena += '<a class="user" href="https://twitter.com/'+ palabra[1:]+'" target="_blank">'+palabra+'</a> '
			#cualquier otra cosa			
			else:
				cadena += palabra + " "

		cadena += '</div>'
		cadena += '<div class="contenedor-rf">'
		cadena += '<span class="fav-count">'
		cadena += str(tweet[1])
		cadena += '</span>'
		cadena += '<span class="retweet-count">'
		cadena += str(tweet[2])
		cadena += '</span>'
		cadena += '</div>'
		cadena += '</div>'

		#tiene algún tipo de objeto multimedia
		if tweet[4] != '':
			cadena += self.imprimeTweettMedia(tweet[4])

		cadena += '</div>'
		return cadena

	def imprimeTweettRelevancia(self, tweet):
		imOrRt = ""

		if tweet[3] == True:
			imOrRt = "rt"
		else:
			imOrRt = "im"

		relevancia = (float(tweet[1]) * 0.75) + (float(tweet[2]) * 1.5)
		if relevancia == 0:
			return '<div class="tweet '+imOrRt+'1">'
		elif relevancia < 100:
			return '<div class="tweet '+imOrRt+'2">'
		elif relevancia < 750:
			return '<div class="tweet '+imOrRt+'3">'
		elif relevancia < 5000:
			return '<div class="tweet '+imOrRt+'4">'
		else:
			return '<div class="tweet '+imOrRt+'5">'

	def imprimeTweettMedia(self, media):
		cadena = ''

		if '.jpg' in media or '.png' in media:
			cadena += '<a href="'+ media +'" target="_blank">'
			cadena += '<div class="img_busqueda" style="background-image: url(\''
			#http://pbs.twimg.com/media/BziK-yaIIAA1uW2.jpg
			cadena += media 
			cadena += '\');">'
		
			cadena += '</div>'
			cadena += '</a>'

		return cadena
