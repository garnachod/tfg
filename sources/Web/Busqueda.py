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
			cadena += '<div class="delimitador"></div>'
			cadena += '<div class="tweet">'
			cadena += tweet[0]
			cadena += '</div>'

		return cadena