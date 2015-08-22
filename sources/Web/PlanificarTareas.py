# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from flask import session
from DBbridge.ConsultasWeb import ConsultasWeb
from SupportWeb import SupportWeb
from WebPageMenu import WebPageMenu

class PlanificarTareas(WebPageMenu):
	def __init__(self):
		super(PlanificarTareas, self).__init__()
		self.head.setTitulo('Planificar Tarea')


	def insertStyles(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/tareas.css")

	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")
		self.head.add_js("static/js/opciones_index.js")
		self.head.add_js("static/js/opciones_generar_tarea.js")

	def mid(self):
		mid = '''
				  <h3 style="text-align: left;" >Planificar tarea:</h3>
					<form action="/alta_tarea" method="post" style="max-width: 500px; margin-left: auto; margin-right: auto;">
						<p style="text-align: left;">Tipo de tarea:</p>
						<p style="text-align: left;">
						<select name="tipoTarea" id="tipoTarea" style="width:339px; margin-left: 70px;">
								<option value="sb">Solo búsqueda</option>
								<option value="bp">Busqueda y análisis de palabras</option>
						</select>
						</p>'''
  		#<option value="bf">Busqueda y análisis de frecuencia</option>
		mid +=	'''	
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
  					'''
  		mid +=   '''				<div id="cont_lista_entrenamiento">
  									<p style="text-align: left;">
  										Lista de tweets usada para el análisis:
  									</p>			
  									<p style="text-align: left;">
	  									<select name="lista_entrenamiento" id="lista_entrenamiento" style="width:339px; margin-left: 70px;">
  					'''
  		rows = self.consultas.getListasEntrenamiento()
		for row in rows:
			mid += '<option value="'+str(row[0])+'">' + row[1] +'</option>'

		mid +=   '''
										</select>
  									</p>
  									</div>
					'''
  		mid +=   '''
  									<p style="margin-bottom: 5px;"><input class="boton-general" type="submit" value="Enviar"></p>
								</form>
				'''
		return SupportWeb.addGeneralStructureMid(mid)

	def scripts(self):
		return ''
