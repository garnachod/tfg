# -*- coding: utf-8 -*-
from Head import Head

class Error():
	def __init__(self):
		self.head = Head('Error')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/error.css")

	def toString(self, codigo):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'
		cadena += '''<div class="header">
						<div class="header-cont">
							
						</div>
					</div>
					<div class="mid">
						<div class="mid-cont">'''
		
		cadena += '''<div class="error-cont">
						<h3>Se ha detectado un error</h3>
						<p>'''	
		cadena += self.getValueCodigo(codigo)
		cadena += '''</p>
						<div class="cont-boton" style="width: 160px; margin-bottom: 20px;">
							<a href="javascript:window.history.back()" class="boton-general">
								Volver atrás
							</a>
						</div>
						<img src="static/img/error.png">
						
					 </div>
				 '''
		cadena +='</div></div>'

		cadena += '</body>'
		return cadena

	def getValueCodigo(self, identificador):
		codigo = { '1': 'Usuario o Contraseña erroneos', '2': 'Parametros a la página incorrectos', '3': 'No tienes permiso de administrador', '4': 'Ruta no permitida', '5': 'No deberias conocer esta ruta joven padawan', '6': 'Error al crear'}
		return codigo[identificador]

