# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from DBbridge.ConsultasWeb import ConsultasWeb
import hashlib

class Login():
	def __init__(self):
		self.head = Head('Login')
		self.generaHead()
		self.consultas = ConsultasWeb()
 
	def generaHead(self):
		self.head.add_css("static/css/general.css")
		self.head.add_css("static/css/login.css")

	def doLogin(self):
		#control de parametros
		
		if request.form['usr'] is None or request.form['pwd'] is None:
			return 'ERR'
		if request.form['usr'] == "" or request.form['pwd'] == "":
			return 'ERR'

		#se busca en la base de datos, se parsea el hash con la contrasenya	
		user, pasw, usr_id = self.consultas.getUserConexionData(request.form['usr'])
		if  user is None:
			return 'ERR'
		else:
			h = hashlib.new('sha256')
   			h.update(request.form['pwd'])
   			pwd = h.hexdigest()

   			if pwd == pasw:
   				#se ha autenticado
   				session['username'] = user
   				session['user_id'] = usr_id

   				return 'OK'
   			else:
   				return 'ERR'

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += '<body>'
		cadena += '''<div class="header">
						<div class="header-cont">
							
						</div>
					</div>
					<div class="mid">
						<div class="mid-cont">'''
		cadena += '''<div class="login-cont">
						<h3>Inicio de sesión</h3>
						<form action="" method="post">
							<p>Usuario:</p>
							<input type="text" name="usr">
							<p>Contraseña:</p>
							<input type="password" name="pwd"><br>
							<p><input class="boton-general" type="submit" value="Enviar"></p>
						</form>
					</div>'''
		cadena +='</div></div>'

		cadena += '</body>'
		return cadena