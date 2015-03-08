# -*- coding: utf-8 -*-
import os
#lib_path = os.path.abspath('../../')
#sys.path.append(lib_path)

from MachineLearning.Clasificadores.RedNeuronal import RedNeuronal
from DBbridge.ConsultasGeneral import ConsultasGeneral
from MachineLearning.PalabrasDeTweet import PalabrasDeTweet
from MachineLearning.RW.LectorARFF import LectorARFF
from MachineLearning.Instance import Instance
from MachineLearning.Instances import Instances
import json


class ClasificadorTweets(object):
	"""docstring for ClasificadorTweets"""
	def __init__(self, id_lista_entrenamiento):
		super(ClasificadorTweets, self).__init__()
		self.clasificador = None
		self.instances = None
		self.consultas = ConsultasGeneral()
		self.columnas = []
		self.diccionarioPalabras = {}
		self.separador = PalabrasDeTweet()
		self.id_lista_entrenamiento = id_lista_entrenamiento
		self.inicializa()


	def inicializa(self):
		row = self.consultas.getFilesLastTrainTweet(self.id_lista_entrenamiento)
	
		if str(os.path.abspath('')) != '/':
			fJSON = open(row[1],'r')
		else:
			fJSON = open('/home/dani/tfg/sources/' + row[1],'r')
		
		self.clasificador = RedNeuronal()
		self.clasificador.restoreClassifierFromJSON(json.load(fJSON))

		lector = LectorARFF()
		if str(os.path.abspath('')) != '/':
			self.instances = lector.soloLeerCabecera(row[0])
		else:
			self.instances = lector.soloLeerCabecera('/home/dani/tfg/sources/' + row[0])
		

		listaDePalabras = self.instances.getColumnasList()
		#inicialización diccionario
		for palabra in listaDePalabras:
			self.diccionarioPalabras[palabra] = 0
			self.columnas.append(palabra)

	def clasificaTweetById(self, idTweet):
		status = self.consultas.getTweetStatus(idTweet)
		return self.clasificaTweetByStatus(status)

		

	def clasificaTweetByStatus(self, status):
		#limpiar las repeticiones
		for palabra in self.diccionarioPalabras:
			self.diccionarioPalabras[palabra] = 0

		cadena = self.separador.removeLinks(status)
		cadena = self.separador.removeTwitterUsers(cadena)
		cadena = self.separador.removeNumbers(cadena)
		palabras = self.separador.getPalabrasFromStringNormalized(cadena)

		#generar las repeticiones
		for palabra in palabras:
			if self.diccionarioPalabras.has_key(palabra):
				self.diccionarioPalabras[palabra] = self.diccionarioPalabras[palabra] + 1

		instance = Instance()
		for palabra in self.columnas:
			instance.addElement(self.diccionarioPalabras[palabra])


		return self.clasificador.classifyInstance(instance)
		



		
		