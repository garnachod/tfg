# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from DBbridge.ConsultasWeb import ConsultasWeb
from UserHeader import UserHeader
from Head import Head
#from DBbridge.ConsultasWeb import ConsultasWeb
import hashlib

class Admin():
	def __init__(self):
		self.head = Head('Admin general')
		self.generaHead()

	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/admin.css")

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'

		consultasWeb = ConsultasWeb()
		userHeader = UserHeader(session["username"], 'static/img/usrIcon.png', consultasWeb.isAdministrator(session['user_id']))
		userHeader.setBotonInicio(True)
		cadena += userHeader.toString()

		cadena += '''<div class="mid">
						<div class="mid-cont">'''
		cadena += '''
					<div class="admin-cont">
					 <div class="cont-form-admin">
						<h3>Creación de un usuario</h3>
						<form action="/admin_new_user" method="post">
							<p>Nombre:</p>
							<input type="text" name="nombre">
							<p>Email:</p>
							<input type="email" name="correo">
							<p>Institución:</p>
							<input type="text" name="institucion">
							<p>Username:</p>
							<input type="text" name="usern">
							<p>Contraseña:</p>
							<input type="password" name="passw">
							<p>Repetir contraseña:</p>
							<input type="password" name="passwr"><br>
							<p><input class="boton-general" type="submit" value="Enviar"></p>
						</form>
					 </div>
					 <div class="cont-form-admin">
						<h3>Añadir claves</h3>
						<form action="/admin_new_apikey" method="post">
							<p>Api Key:</p>
							<input type="text" name="apik">
							<p>Api Key Secret:</p>
							<input type="text" name="apiks">
							<p>Acces Token:</p>
							<input type="text" name="acstoken">
							<p>Acces Token Secret:</p>
							<input type="text" name="acstokens">
							<br>
							<p><input class="boton-general" type="submit" value="Enviar"></p>
						</form>
					 </div>
					</div>
				  '''

		cadena +='</div></div>'

		cadena += '</body>'
		return cadena				