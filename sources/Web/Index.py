# -*- coding: utf-8 -*-
from DBbridge.ConsultasWeb import ConsultasWeb
from UserHeader import UserHeader
from flask import Flask, session, request
from Head import Head
from MenuSlide import MenuSlide
from SupportWeb import SupportWeb
from i18n.i18n import i18n


class Index():
	def __init__(self):
		self.head = Head('index') 
		self.generaHead()
		self.internationalization = i18n()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/opciones_index.js")
		self.head.activaMenu()

	def toString(self,usuario='none'):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		if usuario is 'none':
			cadena += self.toStringNoRegistrado()
		else:
			cadena += self.toStringRegistrado(usuario)

		return cadena
		#session['username']
	def toStringRegistrado(self, usuario):
		cadena = '<body>'
		
		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(usuario, 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']), True)
		cadena += userHeader.toString()

		cadena += SupportWeb.addGeneralStructureMid('''
				<h3 style="text-align:  left;">Búsqueda:</h3>
				<form action="/busqueda" method="post">
					<select name="tipoBusqueda" id="tipoBusqueda">
							<option value="suser">Usuario</option>
							<option value="topic">Contenido</option>
					</select>
					<input id="input_search" type="text" name="search" placeholder="@username">
					<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Buscar"></p>
				</form>
				''')
		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body></html>'
		return cadena

	def toStringNoRegistrado(self):
		lang = request.headers.get('Accept-Language')

		cadena = '<body>'
		cadena += '''<div class="header">
						<div class="header-cont">

						</div>
					</div>
					'''

		medio =  (
					'<h3>'
					''+self.internationalization["session_info_login"][lang]+''
					'</h3>'
					'<div class="cont-boton" style="width: 160px;">'
						'<a href="/login" class="boton-general">'
							'Inicio sesión'
						'</a>'
					'</div>'
					)

		cadena += SupportWeb.addGeneralStructureMid(medio)

		cadena += '</body></html>'
		return cadena