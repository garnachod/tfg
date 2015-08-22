# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from DBbridge.ConsultasWeb import ConsultasWeb
from flask import session
from SupportWeb import SupportWeb
from WebPageMenu import WebPageMenu

class VisualizarListaTareas(WebPageMenu):
	"""docstring for VisualizarListaTareas"""
	def __init__(self):
		super(VisualizarListaTareas, self).__init__()
		self.head.setTitulo('Lista tareas')

	def insertStyles(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/tareas.css")

	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")

	def mid(self):
		tuplas = []
		if self.finalizadas == True:
			tuplas = self.consultas.getTareasTerminadasListado()
		else:
			tuplas = self.consultas.getTareasPendientesListado()

		if tuplas == False:
			return SupportWeb.addGeneralStructureMid('ERR')

		medio  = ('<div class="tarea" style="margin-bottom: 10px;">'
					'<div class="fragmento-tarea claro">Búsqueda</div>'
					'<div class="fragmento-tarea oscuro">Tipo Tarea</div>'
					'<div class="fragmento-tarea claro">Fecha Inicio</div>'
					'<div class="fragmento-tarea oscuro">Fecha Fin</div>'
				'</div>')

		for tupla in tuplas:
			medio += self.generaTareaDeTupla(tupla)

		return SupportWeb.addGeneralStructureMid(medio)

	def scripts(self):
		return ''
		
	def toString(self, finalizadas=False):
		self.finalizadas = finalizadas
		return super(VisualizarListaTareas, self).toString()
		

	def generaTareaDeTupla(self, tupla):
		cadena = '<a href="/resumen_tarea?identificador=' + str(tupla[0]) + '">'
		cadena += '<div class="tarea">'
		cadena += '<div class="fragmento-tarea claro">' + tupla[4] + '</div>'
		cadena += '<div class="fragmento-tarea oscuro">' + tupla[1] + '</div>'
		cadena += '<div class="fragmento-tarea claro">' + str(tupla[2]) + '</div>'
		cadena += '<div class="fragmento-tarea oscuro">' + str(tupla[3]) + '</div>'
		cadena += '</div></a>'

		return cadena
