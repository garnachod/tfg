# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from DBbridge.ConsultasWeb import ConsultasWeb
#from DBbridge.ConsultasWeb import ConsultasWeb
import hashlib


class AdminNewUser():
	def __init__(self):
		self.consultas = ConsultasWeb()

	def add(self):
		nombre = request.form['nombre']
		correo = request.form['correo']
		institucion = request.form['institucion']
		usern = request.form['usern']
		passw = request.form['passw']
		passwr = request.form['passwr']

		if nombre is None or correo is None or institucion is None or usern is None or passw is None or passwr is None:
			return False
		else:
			if passwr == passw:
				h = hashlib.new('sha256')
				h.update(passw)
				contrasenya = h.hexdigest()
				return self.consultas.insertNewUser(nombre, correo, institucion, "normal", usern, contrasenya)
			else:
				return False