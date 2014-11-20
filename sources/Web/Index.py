# -*- coding: utf-8 -*-
from DBbridge.ConsultasWeb import ConsultasWeb
from UserHeader import UserHeader
from flask import Flask, session
from Head import Head



class Index():
	def __init__(self):
		self.head = Head('index') 
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/index.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/opciones_index.js")

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
		userHeader = UserHeader(usuario, 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']))
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-busqueda">
								<h3 style="text-align:  left;">Búsqueda:</h3>
								<form action="/busqueda" method="post">
									<select name="tipoBusqueda" id="tipoBusqueda">
  										<option value="suser">Usuario</option>
  										<option value="topic">Contenido</option>
  									</select>
  									<input id="input_search" type="text" name="search" placeholder="@username">
  									<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Buscar"></p>
								</form>
							</div>
						</div>
					</div>'''

		cadena += '</body>'
		return cadena

	def toStringNoRegistrado(self):
		cadena = '<body>'
		cadena += '''<div class="header">
						<div class="header-cont">'''

		cadena += '''</div>
					</div>
					<div class="mid">
						<div class="mid-cont">
							<div class="ini-ses">
								<h3>
									Debes iniciar sesión en la aplicación
								</h3>
								<div class="cont-boton" style="width: 160px;">
									<a href="/login" class="boton-general">
										Inicio sesión
									</a>
								</div>
							</div>
						</div>
					</div>'''

		cadena += '</body></html>'
		return cadena