class MenuSlide(object):
	"""docstring for MenuSlide"""
	def __init__(self):
		self.menu = True

	def getCSSLib(self):
		return "static/css/jquery.mmenu.all.css"

	def getJSLib(self):
		return "static/js/jquery.mmenu.min.all.js"

	def getJSCode(self):
		code = '<script type="text/javascript">'
		code +=	'$(function() {'
		code +=	'	$("nav#menu").mmenu();'
		code +=	'});'
		code += '</script>'

		return code

	def toStringHead(self):
		return '<a href="#menu"></a>'

	def toStringContenido(self):
		cadena = '<nav id="menu">'
		cadena += '<ul>'
		cadena += '<li><a href="/">Home</a></li>'
		cadena += '<li><a href="/about/">About us</a></li>'
		cadena += '<li><a href="/contact/">Contact</a></li>'
		cadena += '</ul>'
		cadena += '</nav>'

		return cadena
		