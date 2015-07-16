# -*- coding: utf-8 -*-
class UserHeader(object):
	"""docstring for UserHeader"""
	def __init__(self, username, img, admin, menu=False):
		self.username = username
		self.img = img
		self.admin = admin
		self.botonInicio = False
		self.menu = menu

	def toString(self):
		cadena = ''
		cadena += '<nav class="header">'
		if self.menu == True:
			cadena += '<div>'
			cadena += '<a class="boton-menu" href="#menu"></a>'
			cadena += "</div>"
			
		cadena += '<ul class="header-cont">'
		cadena += '<li class="user-header-cont">'
		cadena += '<img src="/' + self.img + '">'				
		cadena += '<h4>'
		cadena += self.username
		cadena += '</h4>'
		#opciones del usuario
		cadena += '<ul>'
		cadena += '<li><a href="cerrar_sesion">Cerrar sesión</a></li>'
		if self.admin == True:
			cadena += '<li><a href="/admin/usuario_nuevo">Panel administración</a></li>'

		cadena += '</ul>'

		#cierre header
		#cierre header-cont
		#cierre user-header-cont
		cadena += '</li>'
		if self.botonInicio == True:
			cadena += '<li class="user-header-cont"><h4><a href="/">Inicio</a></h4></li>'

		cadena += '</ul></nav>'

		return cadena

	def setBotonInicio(self, valor):
		self.botonInicio = valor
		