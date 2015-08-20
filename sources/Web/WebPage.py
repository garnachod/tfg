# -*- coding: utf-8 -*-
from Head import Head
class WebPage(object):
	"""docstring for WebPage"""
	def __init__(self):
		super(WebPage, self).__init__()
		self.head = Head() 
		self.generaHead()

	def generaHead(self):
		raise NotImplementedError( "Should have implemented this" )
	
	
	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += self.header()
		cadena += '<body>'
		cadena += self.mid()
		cadena += self.scripts()
		cadena += '</body>'
		cadena += '</html>'
		return cadena

	def insertStyles(self):
		raise NotImplementedError( "Should have implemented this" )

	def insertScripts(self):
		raise NotImplementedError( "Should have implemented this" )

	def header(self):
		raise NotImplementedError( "Should have implemented this" )

	def mid(self):
		raise NotImplementedError( "Should have implemented this" )

	def scripts(self):
		raise NotImplementedError( "Should have implemented this" )

		
