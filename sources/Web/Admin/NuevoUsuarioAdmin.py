# -*- coding: utf-8 -*-
from Web.Head import Head
from Web.UserHeader import UserHeader
from flask import Flask, session
from DBbridge.ConsultasWeb import ConsultasWeb
from Web.SupportWeb import SupportWeb
from WebPageAdmin import WebPageAdmin

class NuevoUsuarioAdmin(WebPageAdmin):
	"""docstring for NuevoUsuarioAdmin"""
	def __init__(self):
		super(NuevoUsuarioAdmin, self).__init__()
		self.head.setTitulo('Nuevo usuario')

	def insertStyles(self):
		self.head.add_css("/static/css/general.css")
		self.head.add_css("/static/css/admin.css")

	def insertScripts(self):
		pass

	def mid(self):
		mid = """
			<h3>Creación de un usuario</h3>
			<form action="/admin/new_user" method="post">
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
		"""

		return SupportWeb.addGeneralStructureMid(mid) 

	def scripts(self):
		return ''