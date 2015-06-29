from WebPage import WebPage
from DBbridge.ConsultasWeb import ConsultasWeb
from UserHeader import UserHeader
from flask import Flask, session

class WebPageMenu(WebPage):
	"""docstring for WebPageMenu"""
	def __init__(self, botonInicio = True):
		super(WebPageMenu, self).__init__()
		self.consultas = ConsultasWeb()
		self.botonInicio = botonInicio

	def generaHead(self):
		self.insertStyles()
		self.insertScripts()
		self.head.activaMenu()

	def header(self):
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), True)
		userHeader.setBotonInicio(self.botonInicio)
		return userHeader.toString()

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += self.header()
		cadena += '<body>'
		cadena += self.mid()
		cadena += self.head.getMenuInstance().toStringContenido()
		cadena += self.scripts()
		cadena += '</body>'
		cadena += '</html>'
		return cadena

	def insertStyles(self):
		raise NotImplementedError( "Should have implemented this" )

	def insertScripts(self):
		raise NotImplementedError( "Should have implemented this" )

	def mid(self):
		raise NotImplementedError( "Should have implemented this" )

	def scripts(self):
		raise NotImplementedError( "Should have implemented this" )