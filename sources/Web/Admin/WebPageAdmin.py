from Web.WebPageNoMenu import WebPageNoMenu

class WebPageAdmin(WebPageNoMenu):
	"""docstring for WebPageAdmin"""
	def __init__(self):
		super(WebPageAdmin, self).__init__()

	def toString(self):
		cadena = '<!DOCTYPE html>\n<html>'
		cadena += self.head.toString()
		cadena += self.header()
		cadena += '<body>'
		cadena += self.menuAdmin()
		cadena += self.mid()
		cadena += self.scripts()
		cadena += '</body>'
		cadena += '</html>'
		return cadena

	def menuAdmin(self):
		cadena = ( '<div class="cont-menu-admin">'
					'<ul class="menu-admin">'
				   	'<a href="/admin/usuario_nuevo"><li>Nuevo Usuario</li></a>'
				   	'<a href="/admin/nueva_apikey"><li>Nueva ApiKey</li></a>'
				   	'<a href="/admin/estadisticas"><li>Estadisticas Generales</li></a>'
				   	'</ul>'
				   '</div>'
					)
		return cadena