# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from flask import Flask, session
from DBbridge.ConsultasWeb import ConsultasWeb

class PlanificarTareas():
	def __init__(self):
		self.head = Head('Planificar tarea') 
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/tareas.css")
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/opciones_index.js")
		self.head.activaMenu()

	def toString(self, usuario):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()

		cadena += '<body>'
		
		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(usuario, 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">
							<div class="cont-tareas">
								<h3 style="text-align: left;" >Planificar tarea:</h3>
								<form action="/alta_tarea" method="post" style="max-width: 500px; margin-left: auto; margin-right: auto;">
									<p style="text-align: left;">Tipo de tarea:</p>
									<p style="text-align: left;">
									<select name="tipoTarea" id="tipoTarea" style="width:339px; margin-left: 70px;">
  										<option value="sb">Solo búsqueda</option>
  										<option value="bp">Busqueda y análisis de palabras</option>
  										<option value="bf">Busqueda y análisis de frecuencia</option>
  									</select>
  									</p>
  									<p style="text-align: left;">
  										Búsqueda:
  									</p>
  									<p style="text-align: left;">
									<select name="tipoBusqueda" id="tipoBusqueda" style="margin-left: 70px;">
  										<option value="suser">Usuario</option>
  										<option value="topic">Contenido</option>
  									</select>
  									<input id="input_search" type="text" name="search" placeholder="@username" style="text-align: left;">
  									</p>
  									<p style="text-align: left;">
  										Tiempo activo:
  									</p>
  									<p style="text-align: left;">
	  									<select name="tiempoTarea" id="tiempoTarea" style="width:339px; margin-left: 70px;">
	  										<option value="semana">7 días</option>
	  										<option value="dossemana">15 días</option>
	  										<option value="mes">30 días</option> 
	  									</select>
  									</p>
  									<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Enviar"></p>
								</form>
							</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body>'
		return cadena