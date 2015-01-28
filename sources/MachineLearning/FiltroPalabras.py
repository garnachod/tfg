class FiltroPalabras(object):
	"""docstring for FiltroPalabras"""
	def __init__(self):
		super(FiltroPalabras, self).__init__()
		self.palabrasStringEspa = "de;la;que;el;en;y;a;los;se;del;las;un;por;con;no;una;su;para;es;al;lo;como;mas;o;pero;sus;le;ha;me;si;sin;sobre;este;ya;entre;cuando;todo;esta;ser;son;dos;tambien;te"
		self.diccionario = None
		self.generaDiccionarioPalabrasRechazadas()
		
	def generaDiccionarioPalabrasRechazadas(self):
		lista = self.palabrasStringEspa.split(';')
		self.diccionario = {}
		for clave in lista:
			self.diccionario[clave] = True
		#print self.diccionario

	def estaPalabraEnDiccionario(self, palabra):
		return self.diccionario.has_key(palabra)

	def eliminaDeListaPalabras(self, listaPalabras):
		listaRetorno = []
		for palabra in listaPalabras:
			if self.estaPalabraEnDiccionario(palabra):
				pass
			elif palabra == '':
				pass
			else:
				listaRetorno.append(palabra)

		return listaRetorno

"""pruebas unitarias"""
if __name__ == '__main__':
	filtro = FiltroPalabras()
	print 'de'
	print filtro.estaPalabraEnDiccionario('de')
	print 'hola'
	print filtro.estaPalabraEnDiccionario('hola')
	lista = ['hola', 'de', 'los']
	lista = filtro.eliminaDeListaPalabras(lista)
	print lista
