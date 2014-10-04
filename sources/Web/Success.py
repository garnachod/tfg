# -*- coding: utf-8 -*-
from Head import Head

class Success():
	def __init__(self):
		self.head = Head('OK')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/success.css")

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
		
		cadena += '''<div class="success-cont">
						<h3>Se ha completado con éxito</h3>
						<p>'''	
		cadena += self.getValueCodigo(codigo)
		cadena += '''</p>
						<div class="cont-boton" style="width: 160px; margin-bottom: 20px;">
							<a href="javascript:window.history.back()" class="boton-general">
								Volver atrás
							</a>
						</div>
					 </div>
				 '''
		cadena +='</div></div>'

		cadena += '</body>'
		return cadena

	def getValueCodigo(self, identificador):
		codigo = { '1': 'Dar de alta un nuevo usuario', '2': 'Clave creada'}
		return codigo[identificador]