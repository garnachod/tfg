# -*- coding: utf-8 -*-
from Head import Head
from MenuSlide import MenuSlide
from UserHeader import UserHeader
from flask import Flask, session
from DBbridge.ConsultasWeb import ConsultasWeb

class Contacto():
	def __init__(self):
		self.head = Head('index') 
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_js("static/js/jquery.js")
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
							<div class="cont-general">
							<p>Proyecto realizado por Daniel Garnacho Martín</p>
							<p><a href="https://twitter.com/garnachod" target="_blank"><img src="/static/img/twitter_logo.png"></a></p>
							</div>
						</div>
					</div>'''

		menu = self.head.getMenuInstance()
		cadena += menu.toStringContenido()
		cadena += '</body>'
		return cadena

