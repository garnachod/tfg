from heapq import heappush, heappop
from Instance import Instance
from Instances import Instances
from operator import add,mul
import math
from GeneticKNN.IndividuoKNN import IndividuoKNN
import random

class KNNGenetic(object):
	"""docstring for Clasificador"""
	def __init__(self):
		super(KNNGenetic, self).__init__()
		self.data = None
		self.modelo = None
		self.nIndividuos = 20
		self.listaIndividuos = []
		self.nNuevosIndvPorEpoca = 2
		self.nMaxElite = 4
		self.nEpocas = 20

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		self.data = data

		#inicializacion
		for i in range(0 , self.nIndividuos):
			indv = IndividuoKNN(data.getNumeroColumnas() , self.data)
			indv.inicializaRandom()
			self.listaIndividuos.append(indv)

		mejorIndividuo = None
		mejorEpocas = 0

		for epoca in range(0, self.nEpocas):
			if epoca % 2 == 0:
				print epoca

			#cruce
			for i in range(0, self.nIndividuos, 2):
				self.listaIndividuos[i].cruce(self.listaIndividuos[i+1])

			#mutacion
			for indv in self.listaIndividuos:
				indv.mutacion()

			mejorEpoca = 0
			mejorIndvEpoca = None
			arrayCorrectas = []
			sumaCorrectas = 0.0
			for indv in self.listaIndividuos:
				correctas = self.privateClasificaInstanciasReTCount(indv)
				if correctas > mejorEpoca:
					mejorEpoca = correctas
					mejorIndvEpoca = indv.duplica()
				sumaCorrectas += correctas
				arrayCorrectas.append(correctas)

			if mejorEpoca > mejorEpocas:
				mejorEpocas = mejorEpoca
				mejorIndividuo = mejorIndvEpoca

			#print mejorEpoca / float(data.getNumeroInstances())

			#print sumaCorrectas
			for i in range(0, len(arrayCorrectas)):
				arrayCorrectas[i] = arrayCorrectas[i] / sumaCorrectas

			#for correcta in arrayCorrectas:
			#	print correcta

			nuevaListaIndv = []

			for i in range(0, self.nIndividuos - (self.nNuevosIndvPorEpoca + self.nMaxElite)):
				posicion = 0
				suma = 0.0
				aleat = random.random()
				while True:
					suma += arrayCorrectas[posicion]
					#print suma
					if suma >= aleat:
						nuevaListaIndv.append(self.listaIndividuos[posicion])
						break

					posicion += 1

			self.listaIndividuos = nuevaListaIndv

			for i in range(0, self.nNuevosIndvPorEpoca):
				indv = IndividuoKNN(data.getNumeroColumnas() , self.data)
				indv.inicializaRandom()
				self.listaIndividuos.append(indv)

			for i in range(0,  self.nMaxElite):
				#print mejorIndividuo.correctas(data)/ float(data.getNumeroInstances())
				self.listaIndividuos.append(mejorIndividuo.duplica())

			random.shuffle(self.listaIndividuos)
			print mejorEpocas / float(data.getNumeroInstances())
			

		#for indv in self.listaIndividuos:
		#	print indv.correctas(data) / float(data.getNumeroInstances())

		self.modelo = mejorIndividuo.duplica()
		print self.modelo.pesos
		print self.modelo.vecinos
		print mejorEpocas / float(data.getNumeroInstances())

	def privateClasificaInstanciasReTCount(self, individuo):
		countBuena = 0
		for instance in self.data.getListInstances():
			clase = instance.getClase()
			prediccion = individuo.clasifica(instance)

			if prediccion == clase:
				countBuena += 1

		return countBuena

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		return self.modelo.clasifica(instance)

		

	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	def restoreClassifierFromJSON(self, jsonObj):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )

	"""Hace que el clasificador entre en modo debug o no"""
	def setDebug(self, value):
		raise NotImplementedError( "Should have implemented this" )

