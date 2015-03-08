# -*- coding: utf-8 -*-
from Head import Head
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from MenuSlide import MenuSlide
from flask import Flask, session, request

class NuevaListaEntrenamiento(object):
	"""docstring for NuevaListaEntrenamiento"""
	def __init__(self):
		super(NuevaListaEntrenamiento, self).__init__()
		self.head = Head('Listas de entrenamiento')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_js("static/js/jquery.js")
		self.head.activaMenu()

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
							<div class="mid-cont">
								<div class="cont-general">
									<h3 style="text-align: left;">Crear una lista de entrenamiento:</h3>
					   '''

		cadena += '''
						<form method="post">
							Nombre de la lista: 
							<input id="nlista" type="text" name="nlista" placeholder="Nombre" style="text-align: left;">
							<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Crear"></p>
						</form>
				  '''
		cadena += '<h3 style="text-align: left;">listas de entrenamiento:</h3>'
		#crear la cadena de las listas
		cadena += self.generaVistaListas()

		cadena +=  '''
							</div>
						</div>
					</div>'''
		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body></html>'
		return cadena

	def generaVistaListas(self):
		rows = self.consultas.getListasEntrenamiento()
		cadena = ''
		#0 id 1 nombre
		for row in rows:
			cadena += '<div>'
			cadena += '<div class="elemento-listado-sencillo">' + row[1] + '</div>'
			linkBorrado = '/lista_entrena_tweets?borrar_id=' + str(row[0])
			cadena += '<a href="'+linkBorrado+'" class="boton-eliminar">x</a>'
			cadena += '</div>'

		return cadena

	def borrar(self, identificador):
		self.consultas.deleteListaEntrenamiento(identificador)

	def creaLista(self):
		nombre = request.form['nlista']
		if nombre is None:
			return False


		self.consultas.creaListaEntrenamiento(nombre)
		return True