import random
import math   # This will import math module
from src.Instance import Instance
from src.Instances import Instances
from src.Clasificadores.AuxGenetic.Individuo import Individuo
from src.Clasificadores.AuxGenetic.IndividuoNCapas import IndividuoNCapas
from src.Clasificadores.AuxGenetic.IndividuoNCapasECM import IndividuoNCapasECM
from Clasificador import Clasificador
class GeneticECM(Clasificador):
	"""docstring for GeneticECM"""
	def __init__(self):
		super(GeneticECM, self).__init__()
		self.listaIndividuos = []
		self.nIndividuos = 6
		self.nEpocas = 1000
		self.modelo = None
		self.nNuevosIndvPorEpoca = 2
		self.nMaxElite = 4

	def buildClassifier(self, data, test=None):

		#inicializacion
		for i in range(0 , self.nIndividuos):
			indv = IndividuoNCapasECM(data.getClases(), data.getNumeroColumnas())
			indv.inicializaRandom()
			self.listaIndividuos.append(indv)

		mejorEpocas = 0
		mejorIndividuo = None

		for epoca in range(0, self.nEpocas):
			if epoca % 50 == 0:
				print epoca
			#cruce
			for i in range(0, self.nIndividuos, 2):
				self.listaIndividuos[i].cruce(self.listaIndividuos[i+1])

			#mutacion
			for indv in self.listaIndividuos:
				indv.mutacion()


			sumaCorrectas = 0.0
			arrayCorrectas = []
			mejorEpoca = 0
			mejorIndvEpoca = None
			for indv in self.listaIndividuos:
				correctas, ecm = indv.correctas(data)
				correctas = 1.0/ecm
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
				indv = IndividuoNCapasECM(data.getClases(), data.getNumeroColumnas())
				indv.inicializaRandom()
				self.listaIndividuos.append(indv)

			for i in range(0,  self.nMaxElite):
				#print mejorIndividuo.correctas(data)/ float(data.getNumeroInstances())
				self.listaIndividuos.append(mejorIndividuo.duplica())

			random.shuffle(self.listaIndividuos)
			#print 1/mejorEpocas
			

		#for indv in self.listaIndividuos:
		#	print indv.correctas(data) / float(data.getNumeroInstances())

		self.modelo = mejorIndividuo.duplica()

		print mejorEpocas / float(data.getNumeroInstances())



	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instancia):
		clase, ecm = self.modelo.clasifica(instancia)
		return clase

