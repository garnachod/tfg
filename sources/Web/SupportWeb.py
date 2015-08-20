# -*- coding: utf-8 -*-
class SupportWeb(object):
	"""Proporciona funciones utiles para mejorar la interfaz web"""
	@staticmethod
	def addGeneralStructureMid(cadena=""):
		try:
			retorno = '<div class="mid">'
			retorno += '<div class="mid-cont">'
			retorno += '<div class="cont-general">'

		
			retorno += cadena

			
			
			retorno += '</div></div></div>'
					  
			return retorno
		except Exception, e:
			print cadena
			print e
			return ""