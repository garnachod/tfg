class ConjuntoPalabras(object):
	"""docstring for ConjuntoPalabras"""
	def __init__(self):
		super(ConjuntoPalabras, self).__init__()
		self.diccionario = {}

	def addListaPalabras(self, listaPalabras):
		for palabra in listaPalabras:
			if self.diccionario.has_key(palabra):
				self.diccionario[palabra] = self.diccionario[palabra] + 1
			else:
				self.diccionario[palabra] = 1

	def getListaPalabras(self):
		return self.diccionario.keys()

	def getListaPalabrasRepMayorQue(self, nRep):
		lista = []

		for clave in self.diccionario:
			if self.diccionario[clave] > nRep:
				lista.append(clave)

		return lista
		