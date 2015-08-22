# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from flask import session
from DBbridge.ConsultasWeb import ConsultasWeb
from SupportWeb import SupportWeb
from WebPageMenu import WebPageMenu

class Contacto(WebPageMenu):
	def __init__(self):
		super(Contacto, self).__init__()
		self.head.setTitulo('Contacto')

	def insertStyles(self):
		self.head.add_css("static/css/general.css")

	def insertScripts(self):
		self.head.add_js("static/js/jquery.js")

	def mid(self):
		return SupportWeb.addGeneralStructureMid('''
					<p>Proyecto realizado por Daniel Garnacho Martín</p>
					<p><a href="https://twitter.com/garnachod" target="_blank"><img src="/static/img/twitter_logo.png"></a></p>
				  ''')

	def scripts(self):
		return ''

