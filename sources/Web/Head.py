
class Head():
	"""docstring for Head""" 
	def __init__(self, titulo):
		self.lista_css = []
		self.lista_js =[]
		self.titulo = titulo

	def add_css(self, css):
		self.lista_css.append(css)

	def add_js(self, js):
		self.lista_js.append(js)

	def toString(self):
		cadena = '<head>'
		cadena += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
		cadena += '<title>'+ self.titulo +'</title>'
		for css in self.lista_css:
			cadena += '<LINK href="'+css+'" rel="stylesheet" type="text/css">'

		for js in self.lista_js:
			cadena += '<script src="'+js+'" language="JavaScript"> </script>'

		cadena += '</head>'
		return cadena