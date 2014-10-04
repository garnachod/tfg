# -*- coding: utf-8 -*-
from flask import Flask, session
from Head import Head


class Index():
	def __init__(self):
		self.head = Head('index') 
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/index.css")

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
		cadena += '''<div class="header">
						<div class="header-cont">'''
		cadena += '''<div class="user-header-cont">
						<img src="static/img/usrIcon.png">
				  		<h4>'''
		cadena += usuario
		cadena +='''</h4></div>'''
		cadena += '''</div>
					</div>
					<div class="mid">
						<div class="mid-cont">
							<div class="cont-busqueda">
								<h3 style="text-align:  left;">Búsqueda:</h3>
								<form action="/busqueda" method="post">
									<select name="tipoBusqueda">
  										<option value="suser">Usuario</option>
  									</select>
  									<input type="text" name="search" placeholder="@username">
  									<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Buscar"></p>
								</form>
							</div>
							<div class="cont-resultados">
								<h3>Aquí los resultados</h3>
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

		cadena += '</body>'
		return cadena