# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from flask import Flask, session

class VisualizarListaTareas(object):
	"""docstring for VisualizarListaTareas"""
	def __init__(self):
		super(VisualizarListaTareas, self).__init__()
		self.head = Head('Lista tareas')
		self.consultas = ConsultasWeb()
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/tareas.css")
		self.head.add_js("static/js/jquery.js")
		self.head.activaMenu()

	def toString(self, finalizadas=False):

		tuplas = []
		if finalizadas == True:
			tuplas = self.consultas.getTareasTerminadasListado()
		else:
			tuplas = self.consultas.getTareasPendientesListado()

		if tuplas == False:
			return 'ERR'

		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-tareas">'''

		cadena += '<div class="tarea" style="margin-bottom: 10px;">'
		cadena += '<div class="fragmento-tarea claro">Búsqueda</div>'
		cadena += '<div class="fragmento-tarea oscuro">Tipo Tarea</div>'
		cadena += '<div class="fragmento-tarea claro">Fecha Inicio</div>'
		cadena += '<div class="fragmento-tarea oscuro">Fecha Fin</div>'
		cadena += '</div>'

		for tupla in tuplas:
			cadena += self.generaTareaDeTupla(tupla)

		cadena +='''</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body>'
		return cadena

	def generaTareaDeTupla(self, tupla):
		cadena = ''
		cadena += '<div class="tarea">'
		cadena += '<div class="fragmento-tarea claro">' + tupla[4] + '</div>'
		cadena += '<div class="fragmento-tarea oscuro">' + tupla[1] + '</div>'
		cadena += '<div class="fragmento-tarea claro">' + str(tupla[2]) + '</div>'
		cadena += '<div class="fragmento-tarea oscuro">' + str(tupla[3]) + '</div>'
		cadena += '</div>'

		return cadena
