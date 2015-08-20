# -*- coding: utf-8 -*-
from MenuSlide import MenuSlide

class Head():
	"""docstring for Head""" 
	def __init__(self, titulo=""):
		self.lista_css = []
		self.lista_js =[]
		self.titulo = titulo
		self.menu = False
		self.menuInstance = MenuSlide()

	def setTitulo(self, titulo):
		self.titulo = titulo

	def activaMenu(self):
		self.menu = True
		self.lista_css.append(self.menuInstance.getCSSLib())
		self.lista_js.append(self.menuInstance.getJSLib())

	def add_css(self, css):
		self.lista_css.append(css)

	def add_js(self, js):
		self.lista_js.append(js)

	def getMenuInstance(self):
		return self.menuInstance

	def toString(self):
		cadena = '<head>'
		cadena += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
		cadena += '<meta name="viewport" content="width=device-width, user-scalable=no">'
		cadena += '<title>'+ self.titulo +'</title>'
		for css in self.lista_css:
			cadena += '<link href="'+css+'" rel="stylesheet" type="text/css">'


		for js in self.lista_js:
			cadena += '<script src="'+js+'" language="JavaScript"> </script>'

		if self.menu == True:
			cadena += self.menuInstance.getJSCode()

		cadena += '</head>'
		return cadena