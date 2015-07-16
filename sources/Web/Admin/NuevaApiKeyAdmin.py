# -*- coding: utf-8 -*-
from Web.Head import Head
from Web.UserHeader import UserHeader
from flask import Flask, session
from DBbridge.ConsultasWeb import ConsultasWeb
from Web.SupportWeb import SupportWeb
from WebPageAdmin import WebPageAdmin

class NuevaApiKeyAdmin(WebPageAdmin):
	"""docstring for NuevaApiKeyAdmin"""
	def __init__(self):
		super(NuevaApiKeyAdmin, self).__init__()
		
	def insertStyles(self):
		self.head.add_css("/static/css/general.css")
		self.head.add_css("/static/css/admin.css")

	def insertScripts(self):
		pass

	def mid(self):
		mid = """
			<h3>Añadir claves</h3>
			<form action="/admin/new_apikey" method="post">
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
			"""

		return SupportWeb.addGeneralStructureMid(mid) 

	def scripts(self):
		return ''