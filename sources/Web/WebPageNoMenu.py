# -*- coding: utf-8 -*-
from WebPage import WebPage
from DBbridge.ConsultasWeb import ConsultasWeb
from UserHeader import UserHeader
from flask import session

class WebPageNoMenu(WebPage):
	"""docstring for WebPageMenu"""
	def __init__(self, botonInicio = True):
		super(WebPageNoMenu, self).__init__()
		self.consultas = ConsultasWeb()
		self.botonInicio = botonInicio

	def generaHead(self):
		self.insertStyles()
		self.insertScripts()

	def header(self):
		userHeader = UserHeader(session['username'], 'static/img/usrIcon.png', self.consultas.isAdministrator(session['user_id']), False)
		userHeader.setBotonInicio(self.botonInicio)
		return userHeader.toString()

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

	def mid(self):
		raise NotImplementedError( "Should have implemented this" )

	def scripts(self):
		raise NotImplementedError( "Should have implemented this" )