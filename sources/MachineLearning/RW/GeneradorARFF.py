# -*- coding: utf-8 -*-
#import os, sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)

from DBbridge.ConsultasGeneral import ConsultasGeneral
from MachineLearning.ListaPalabrasEntrenamiento import ListaPalabrasEntrenamiento
from MachineLearning.ConjuntoPalabras import ConjuntoPalabras
from MachineLearning.FiltroPalabras import FiltroPalabras
from MachineLearning.PalabrasDeTweet import PalabrasDeTweet

class GeneradorARFF(object):
	"""docstring for GeneradorARFF"""
	def __init__(self):
		super(GeneradorARFF, self).__init__()
		self.consultas = ConsultasGeneral()
		self.clases = []
		self.columnas = []
		self.filas = []
	
	def entrenamientoTweets(self, nombreFichero, id_lista_entrenamiento):
		listaDePalabrasClass = ListaPalabrasEntrenamiento()
		listaDePalabras = listaDePalabrasClass.getTweetsAndTransform()

		diccionarioPalabras = {}
		#inicialización diccionario
		for palabra in listaDePalabras:
			diccionarioPalabras[palabra] = 0
			self.columnas.append(palabra)

		separador = PalabrasDeTweet()
		conjunto = ConjuntoPalabras()
		tweetsAndClass = self.consultas.getTweetsAndClassTrain(id_lista_entrenamiento)

		for tweet in tweetsAndClass:
			cadena = tweet[0]
			cadena = separador.removeLinks(cadena)
			cadena = separador.removeTwitterUsers(cadena)
			cadena = separador.removeNumbers(cadena)
			palabras = separador.getPalabrasFromStringNormalized(cadena)

			#generar las repeticiones
			for palabra in palabras:
				if diccionarioPalabras.has_key(palabra):
					diccionarioPalabras[palabra] = diccionarioPalabras[palabra] + 1

			#pasar las generaciones a la tabla
			fila = []
			for palabra in listaDePalabras:
				fila.append(diccionarioPalabras[palabra])
			#	insertar la clase
			fila.append(tweet[1])
			#	insertar la fila en la tabla
			self.filas.append(fila)
			#limpiar las repeticiones
			for palabra in listaDePalabras:
				diccionarioPalabras[palabra] = 0

		#escribir fichero
		f = open(nombreFichero,'w')
		#escribir cabecera
		f.write('@RELATION tweets\n')
		for palabra in self.columnas:
			f.write('@ATTRIBUTE ')
			f.write(palabra)
			f.write(' REAL')
			f.write('\n')

		#@ATTRIBUTE sepallength	REAL
		#@ATTRIBUTE sepalwidth 	REAL
		#@ATTRIBUTE petallength 	REAL
		#@ATTRIBUTE petalwidth	REAL
		f.write('\n@ATTRIBUTE class {no_relevante,relevante}\n')
		

		f.write('\n@DATA\n')

		for fila in self.filas:
			primero = True
			for elem in fila:
				if primero == True:
					primero = False
					f.write(str(elem))
				else:
					f.write(',')
					f.write(str(elem))

			f.write('\n')

		f.close() # 

"""pruebas unitarias"""
if __name__ == '__main__':
	deb = GeneradorARFF()
	deb.entrenamientoTweets('test.arff')
		