import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from DBbridge.ConsultasGeneral import ConsultasGeneral
from ConjuntoPalabras import ConjuntoPalabras
from FiltroPalabras import FiltroPalabras
from PalabrasDeTweet import PalabrasDeTweet

class ListaPalabrasEntrenamiento(object):
	"""docstring for ListaPalabrasEntrenamiento"""
	def __init__(self):
		super(ListaPalabrasEntrenamiento, self).__init__()
		self.consultas = ConsultasGeneral()

	def getDebugTweetAndTransform(self):
		separador = PalabrasDeTweet()
		conjunto = ConjuntoPalabras()
		for identificador in range(7922,10000):
			cadena = self.consultas.getTweetDebugMachineLearning(identificador)
			cadena = separador.removeLinks(cadena)
			cadena = separador.removeTwitterUsers(cadena)
			cadena = separador.removeNumbers(cadena)
			conjunto.addListaPalabras(separador.getPalabrasFromStringNormalized(cadena))

		filtro = FiltroPalabras()
		return filtro.eliminaDeListaPalabras(conjunto.getListaPalabrasRepMayorQue(2))

	def getTweetsAndTransform(self):
		separador = PalabrasDeTweet()
		conjunto = ConjuntoPalabras()
		listaIDS = self.consultas.getIDTweetsTrainList()

		for identificador in listaIDS:
			cadena = self.consultas.getTweetStatus(identificador)
			cadena = separador.removeLinks(cadena)
			cadena = separador.removeTwitterUsers(cadena)
			cadena = separador.removeNumbers(cadena)
			conjunto.addListaPalabras(separador.getPalabrasFromStringNormalized(cadena))

		filtro = FiltroPalabras()
		return filtro.eliminaDeListaPalabras(conjunto.getListaPalabrasRepMayorQue(0))
	
"""pruebas unitarias"""
if __name__ == '__main__':
	debug = ListaPalabrasEntrenamiento()
	#lista =  debug.getDebugTweetAndTransform();
	lista = debug.getTweetsAndTransform()
	print lista
	print "tamanyo"
	print len(lista)